'use client';

import { useState } from 'react';

// Define the types for our form state
interface Criterion {
  description: string;
  points: number;
}

export default function CreateRubric() {
  const [assignmentId, setAssignmentId] = useState<number>(1); // Placeholder
  const [rubricName, setRubricName] = useState<string>('New Rubric');
  const [criteria, setCriteria] = useState<Criterion[]>([
    { description: 'Correctness', points: 10 },
  ]);
  const [statusMessage, setStatusMessage] = useState<string>('');

  const handleAddCriterion = () => {
    setCriteria([...criteria, { description: '', points: 5 }]);
  };

  const handleCriterionChange = (index: number, field: keyof Criterion, value: string | number) => {
    const newCriteria = [...criteria];
    const criterionToUpdate = { ...newCriteria[index] };
    
    if (field === 'points' && typeof value === 'string') {
        criterionToUpdate[field] = parseInt(value, 10) || 0;
    } else if (field === 'description' && typeof value === 'string') {
        criterionToUpdate[field] = value;
    }
    
    newCriteria[index] = criterionToUpdate;
    setCriteria(newCriteria);
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setStatusMessage('Submitting...');

    const rubricData = {
      assignment_id: assignmentId,
      name: rubricName,
      criteria: criteria,
    };

    try {
      const response = await fetch('http://127.0.0.1:8000/api/rubrics/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(rubricData),
      });

      if (!response.ok) {
        throw new Error('Network response was not ok');
      }

      const result = await response.json();
      setStatusMessage(`Successfully created rubric with ID: ${result.id}`);
    } catch (error) {
      console.error('Failed to create rubric:', error);
      setStatusMessage('Failed to create rubric.');
    }
  };

  return (
    <main style={{ fontFamily: 'sans-serif', padding: '2rem', maxWidth: '800px', margin: 'auto' }}>
      <h1>Create a New Rubric</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Assignment ID:</label>
          <input
            type="number"
            value={assignmentId}
            onChange={(e) => setAssignmentId(parseInt(e.target.value))}
            required
            style={{ marginLeft: '10px', padding: '5px' }}
          />
        </div>
        <div style={{ marginTop: '1rem' }}>
          <label>Rubric Name:</label>
          <input
            type="text"
            value={rubricName}
            onChange={(e) => setRubricName(e.target.value)}
            required
            style={{ marginLeft: '10px', padding: '5px' }}
          />
        </div>

        <h2 style={{ marginTop: '2rem' }}>Criteria</h2>
        {criteria.map((criterion, index) => (
          <div key={index} style={{ marginBottom: '1rem', display: 'flex', gap: '10px' }}>
            <input
              type="text"
              placeholder="Criterion description"
              value={criterion.description}
              onChange={(e) => handleCriterionChange(index, 'description', e.target.value)}
              style={{ flex: 3, padding: '5px' }}
            />
            <input
              type="number"
              placeholder="Points"
              value={criterion.points}
              onChange={(e) => handleCriterionChange(index, 'points', e.target.value)}
              style={{ flex: 1, padding: '5px' }}
            />
          </div>
        ))}
        
        <button type="button" onClick={handleAddCriterion}>
          + Add Criterion
        </button>
        <button type="submit" style={{ marginLeft: '1rem', fontWeight: 'bold' }}>
          Save Rubric
        </button>
      </form>
      {statusMessage && <p style={{ marginTop: '1rem' }}>{statusMessage}</p>}
    </main>
  );
}