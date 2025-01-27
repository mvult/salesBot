import { useState } from 'react';
import { useUpdateAgent, useCreateAgent } from '@/services/useAgents';

export const AgentInput = ({ agent, back }) => {
  // Separate states for each field
  const [name, setName] = useState(agent?.name || '');
  const [model, setModel] = useState(agent?.model || 'claude-3-5-sonnet-latest');
  const [tools, setTools] = useState(JSON.stringify(agent?.tools, null, 2) || '');
  const [identity, setIdentity] = useState(agent?.identity || '');
  const [instructions, setInstructions] = useState(agent?.instructions || '');

  const createAgent = useCreateAgent();
  const updateAgent = useUpdateAgent();
  console.log("agent.model", agent?.model, model)

  const handleToolsEdit = (e) => {
    console.log(e)
    try {
      const tmp = JSON.parse(e);
      setTools(JSON.stringify(tmp, null, 2));
    } catch (e) {
      console.log(e)
    }
  }

  const agentData = { name, model, identity, tools, instructions };

  return (
    <div className="max-w-4xl mx-auto w-400 p-6 rounded-lg shadow-md">
      {/* Name Input */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Name
        </label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          placeholder="Agent name"
        />
      </div>

      {/* Model Selection */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Model
        </label>
        <select
          value={model}
          onChange={(e) => setModel(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="claude-3-5-sonnet-latest">claude-3-5-sonnet-latest</option>
          <option value={model}>{model}</option>
        </select>
      </div>

      {/* Tools Input */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Tools
        </label>
        <textarea
          value={tools}
          onChange={(e) => handleToolsEdit(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          rows="4"
          placeholder="Enter tools configuration..."
        />
      </div>

      {/* Identity Input */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Identity
        </label>
        <textarea
          value={identity}
          onChange={(e) => setIdentity(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
          rows="4"
          placeholder="Define agent identity..."
        />
      </div>

      {/* Instructions Input */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-300 mb-2">
          Instructions
        </label>
        <textarea
          value={instructions}
          onChange={(e) => setInstructions(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:border-blue-500 min-h-[200px]"
          rows="8"
          placeholder="Detailed instructions for the agent..."
        />
      </div>
      {agent ?
        <button
          disabled={updateAgent.isPending}
          onClick={() => {
            updateAgent.mutate({ id: agent.id, agentData },
              { onSuccess: () => back(), onError: (error) => alert(`Update failed: ${error}`) })
          }}
          className="mr-2 bg-gray-700"
        >
          Save Changes
        </button> :
        <button
          disabled={createAgent.isPending}
          onClick={() => { createAgent.mutate(agentData); back() }}
          className="mr-2 bg-gray-700"
        >
          Create New Agent
        </button>
      }

    </div>
  );
}
