import { describe, it, expect } from 'vitest';
import { render, screen } from '../utils/test-utils';
import App from '../../App';

describe('App', () => {
  it('renders the count button', () => {
    render(<App />);
    const button = screen.getByRole('button', { name: /count is/i });
    expect(button).toBeInTheDocument();
  });
});
