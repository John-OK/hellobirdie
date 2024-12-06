import React, { useState } from 'react';

function TestHooks() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <h1>Test Component</h1>
      <p>Count: {count}</p>
      <button onClick={() => setCount(count + 1)}>Increment</button>
    </div>
  );
}

export default TestHooks;
