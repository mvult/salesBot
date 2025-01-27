

export const AgentItem = ({ agent, selectAgent }) => {
  return (
    <div className="p-4 my-4 bg-gray-300 border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow" onClick={selectAgent}>
      <h2 className="text-xl font-semibold text-gray-800">{agent.name}</h2>
      <p className="text-sm text-gray-600 mt-1">{agent.model}</p>
    </div>
  );
}
