import { render, screen } from '@testing-library/react';
import App from './App';

test('renders the trade form', () => {
  render(<App />);
  const headingElement = screen.getByText(/Create Trade/i);
  expect(headingElement).toBeInTheDocument();
});

test('renders the positions table', () => {
  render(<App />);
  const headingElement = screen.getByText(/Open Positions/i);
  expect(headingElement).toBeInTheDocument();
});
