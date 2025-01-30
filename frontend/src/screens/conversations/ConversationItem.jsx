import { useAgents } from '@/services/useAgents';

const ConversationItem = ({ conversation, onClick }) => {
  const { data: agents } = useAgents();

  const agent_name = agents?.find(agent => agent.id === conversation.agent_id)?.name;

  return (
    <div
      onClick={onClick}
      className="bg-white rounded-lg shadow-md mb-4 p-4 cursor-pointer hover:bg-gray-50 transition-colors"
    >
      <div className="flex justify-between items-center">
        <h2 className="text-xl text-gray-800 font-semibold">
          {conversation.client_name || `Client ${conversation.client_id}`}
        </h2>
        <div className="flex gap-2">
          {conversation.handed_off && (
            <span className="px-2 py-1 text-sm bg-yellow-100 text-yellow-800 rounded-full">
              Handed Off
            </span>
          )}
          {conversation.archived && (
            <span className="px-2 py-1 text-sm bg-gray-100 text-gray-800 rounded-full">
              Archived
            </span>
          )}
        </div>
      </div>
      <div className="mt-2 text-sm text-gray-600">
        <p>Platform: {conversation.platform || 'N/A'}</p>
        <p>Agent: {agent_name || 'N/A'}</p>
        {conversation.outcome && (
          <p className="mt-1">Outcome: {conversation.outcome}</p>
        )}
      </div>
    </div>
  );
};

export default ConversationItem;
