import { run } from 'uebersicht';

// Note: Ensure this PROJECT_DIR points to the absolute path where the project resides.
const PROJECT_DIR = '/Users/kalyaangurudevkk/Git/Striver_tracker_widget';

export const command = `
  cd ${PROJECT_DIR} && 
  /usr/bin/env python3 src/tracker.py > /dev/null 2>&1 &&
  cat data/progress.json
`;

// Refresh every 60 seconds
export const refreshFrequency = 60000;

export const className = `
  top: 20px;
  right: 20px;
  color: #fff;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  background-color: rgba(20, 20, 25, 0.85);
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  width: 300px;
`;

export const render = ({ output, error }) => {
  if (error) {
    return (
      <div>
        <h3 style={{ margin: '0 0 15px 0', fontSize: '16px', fontWeight: '600' }}>Striver DSA</h3>
        <p style={{ color: '#ff6b6b', fontSize: '12px' }}>Error executing script: {String(error)}</p>
      </div>
    );
  }

  if (!output) {
    return (
      <div>
        <h3 style={{ margin: '0 0 15px 0', fontSize: '16px', fontWeight: '600' }}>Striver DSA</h3>
        <p style={{ color: '#adb5bd', fontSize: '12px' }}>Loading progress...</p>
      </div>
    );
  }

  let data;
  try {
    data = JSON.parse(output);
  } catch (e) {
    return (
      <div>
        <h3 style={{ margin: '0 0 15px 0', fontSize: '16px', fontWeight: '600' }}>Striver DSA</h3>
        <p style={{ color: '#ff6b6b', fontSize: '12px' }}>Failed to parse JSON.</p>
      </div>
    );
  }

  const { total, completed, percentage, topics } = data;

  // Calculate weak topics (lowest percentage completion)
  const weakTopics = Object.entries(topics || {})
    .map(([name, stats]) => {
      const p = stats.total > 0 ? (stats.done / stats.total) * 100 : 100;
      return { name, done: stats.done, total: stats.total, percentage: p };
    })
    .sort((a, b) => a.percentage - b.percentage)
    .slice(0, 3); // top 3 weakest

  return (
    <div>
      <h3 style={{ margin: '0 0 15px 0', fontSize: '16px', fontWeight: '600', color: '#e0e0e0', display: 'flex', justifyContent: 'space-between' }}>
        <span>Striver A2Z Sheet</span>
        <span style={{ color: '#4dabf7' }}>{percentage.toFixed(1)}%</span>
      </h3>

      <div style={{ marginBottom: '20px' }}>
        <div style={{ width: '100%', backgroundColor: 'rgba(255, 255, 255, 0.1)', borderRadius: '4px', height: '8px', overflow: 'hidden' }}>
          <div style={{ width: \`\${percentage}%\`, backgroundColor: '#4dabf7', height: '100%', transition: 'width 0.5s ease-in-out' }}></div>
        </div>
        <div style={{ fontSize: '12px', color: '#adb5bd', marginTop: '6px', textAlign: 'right' }}>
          {completed} / {total} Solved
        </div>
      </div>

      <h4 style={{ margin: '0 0 10px 0', fontSize: '13px', fontWeight: '500', color: '#ced4da', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '4px' }}>
        Focus Areas
      </h4>
      <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
        {weakTopics.map(topic => (
          <div key={topic.name} style={{ display: 'flex', justifyContent: 'space-between', fontSize: '13px' }}>
            <span style={{ color: '#f8f9fa' }}>{topic.name}</span>
            <span style={{ color: '#adb5bd' }}>
              {topic.done}/{topic.total} ({topic.percentage.toFixed(0)}%)
            </span>
          </div>
        ))}
      </div>
    </div>
  );
};
