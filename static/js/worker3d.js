import React from 'react';
import { createRoot } from 'react-dom/client';
import Spline from '@splinetool/react-spline';

// Universal 3D React Component for Daily Wage Workers
function Worker3DComponent() {
  return React.createElement(
    'div',
    { 
      style: { 
        position: 'fixed', 
        bottom: '20px', 
        right: '20px', 
        width: '300px', 
        height: '300px', 
        zIndex: 9999, 
        pointerEvents: 'none', // Lets clicks pass through the wrapper so it doesn't block UI
        filter: 'drop-shadow(0px 10px 20px rgba(0,0,0,0.15))'
      } 
    },
    React.createElement(
      'div',
      { style: { pointerEvents: 'auto', width: '100%', height: '100%' } }, // Allows mouse interaction with the 3D model
      React.createElement(Spline, { 
        // Using a generic 3D character/worker scene placeholder
        scene: 'https://prod.spline.design/6Wq1Q7YGyM-iab9i/scene.splinecode' 
      })
    )
  );
}

const rootElement = document.getElementById('react-3d-root');
if (rootElement) {
  const root = createRoot(rootElement);
  root.render(React.createElement(Worker3DComponent));
}
