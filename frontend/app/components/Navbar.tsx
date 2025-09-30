// In file: frontend/app/components/Navbar.tsx
import Link from 'next/link';

export default function Navbar() {
  const navStyle = {
    backgroundColor: '#222',
    padding: '1rem 2rem',
    display: 'flex',
    gap: '2rem',
    alignItems: 'center',
  };

  const linkStyle = {
    color: 'white',
    textDecoration: 'none',
    fontSize: '16px',
  };

  const logoStyle = {
    ...linkStyle,
    fontWeight: 'bold',
    fontSize: '20px',
  };

  return (
    <nav style={navStyle}>
      <Link href="/" style={logoStyle}>Neo-Tutor</Link>
      <Link href="/rubrics/create" style={linkStyle}>Create Rubric</Link>
      <Link href="/upload" style={linkStyle}>Upload Flowchart</Link>
    </nav>
  );
}