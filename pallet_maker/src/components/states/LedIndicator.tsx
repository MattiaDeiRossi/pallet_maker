import React from 'react';

type Props = {
  color: 'red' | 'green' | 'blue';
  size: number;
};

const LedIndicator: React.FC<Props> = ({ color, size }) => {
  return (
    <div
      style={{
        width: size,
        height: size,
        borderRadius: '50%',
        backgroundColor: color,
        boxShadow: `0 0 10px ${color}`,
        border: '1px solid #888',
        display: 'inline-block',
      }}
    />
  );};

export default LedIndicator;
