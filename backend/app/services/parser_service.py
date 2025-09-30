import docx
import io
import cv2
import numpy as np
import pytesseract
from fastapi import UploadFile

# ... (tesseract_cmd line and parse_docx function remain the same) ...

# ----------------- HELPER FUNCTIONS -----------------
def get_shape_center(contour):
    """Calculates the center of a contour."""
    M = cv2.moments(contour)
    if M["m00"] == 0:
        return (0, 0)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return (cX, cY)

def find_closest_shape(point, shapes):
    """Finds which shape a point is closest to."""
    closest_shape = None
    min_dist = float('inf')
    for shape in shapes:
        shape_center = get_shape_center(shape["contour"])
        dist = np.linalg.norm(np.array(point) - np.array(shape_center))
        if dist < min_dist:
            min_dist = dist
            closest_shape = shape
    return closest_shape

# ----------------- MAIN PARSER FUNCTION -----------------
def parse_image(file: bytes):
    """
    Identifies shapes, text, and arrows to build a flowchart graph.
    """
    nparr = np.frombuffer(file, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    
    # 1. Find all contours (shapes and arrows)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    shapes = []
    arrows = []
    
    # 2. Identify and separate shapes from arrows
    for i, contour in enumerate(contours):
        area = cv2.contourArea(contour)
        if area < 1000: # Filter out small noise
            continue
            
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
        
        # Assume larger area contours are shapes and smaller ones are potential arrows
        if area > 8000: # This threshold may need tuning
            shape_type = "Unknown"
            if len(approx) == 4:
                shape_type = "Rectangle/Diamond"
            elif len(approx) > 4:
                shape_type = "Oval"

            x, y, w, h = cv2.boundingRect(contour)
            roi = gray[y:y+h, x:x+w]
            text = pytesseract.image_to_string(roi, config='--psm 6').strip()
            
            shapes.append({
                "id": i + 1,
                "shape": shape_type,
                "text": text if text else "No text found",
                "contour": contour
            })
        else:
            arrows.append(contour)

    # 3. Map connections by analyzing arrows
    edges = []
    for arrow_contour in arrows:
        # Find the start (tail) and end (head) of the arrow
        # This is a simplified approach; more advanced methods exist
        # We find the center of the arrow and assume the point on its contour
        # furthest from the center is the head.
        arrow_center = get_shape_center(arrow_contour)
        
        max_dist = -1
        arrow_head = None
        for point in arrow_contour:
            dist = np.linalg.norm(np.array(point[0]) - np.array(arrow_center))
            if dist > max_dist:
                max_dist = dist
                arrow_head = tuple(point[0])
        
        # The tail is roughly opposite the head
        arrow_tail = (2 * arrow_center[0] - arrow_head[0], 2 * arrow_center[1] - arrow_head[1])

        # Find which shapes the head and tail are closest to
        from_shape = find_closest_shape(arrow_tail, shapes)
        to_shape = find_closest_shape(arrow_head, shapes)

        if from_shape and to_shape and from_shape["id"] != to_shape["id"]:
            edges.append({
                "from": from_shape["id"],
                "to": to_shape["id"]
            })
    
    # 4. Assemble the final graph
    # We remove the raw contour data before returning the JSON
    final_nodes = [{"id": s["id"], "shape": s["shape"], "text": s["text"]} for s in shapes]

    return {"nodes": final_nodes, "edges": edges}


# ... (keep the parse_pdf and parse_file functions as is) ...