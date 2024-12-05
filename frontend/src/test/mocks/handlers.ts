import { rest } from 'msw';

// Define handlers for mock API endpoints
export const handlers = [
  // Health check endpoint
  rest.get('/api/health', (req, res, ctx) => {
    return res(ctx.status(200), ctx.json({ status: 'ok' }));
  }),
];
