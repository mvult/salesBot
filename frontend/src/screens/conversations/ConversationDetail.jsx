import { useDeleteConversation, useUpdateConversation } from '@/services/useConversations';

import { MessageList } from './MessageList';

const ConversationDetail = ({ conversation, onBack }) => {
  const { mutate: deleteConversation } = useDeleteConversation();
  const { mutate: updateConversation } = useUpdateConversation();

  if (!conversation) return null;

  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this conversation?')) {
      deleteConversation(conversation.id);
      onBack();
    }
  };

  const handleArchiveToggle = () => {
    updateConversation({
      id: conversation.id,
      conversationData: { archived: !conversation.archived }
    });
  };

  const handleOutcomeChange = (outcome) => {
    updateConversation({
      id: conversation.id,
      conversationData: { outcome }
    });
  };

  return (
    <div className="p-6">
      <button
        onClick={onBack}
        className="mb-4 text-blue-600 hover:text-blue-800 flex items-center"
      >
        ← Back to Conversations
      </button>

      <div className="bg-white rounded-lg shadow-md p-6">
        <div className="flex justify-between items-center mb-4">
          <h1 className="text-xl font-bold text-gray-800 pr-6">
            {conversation.client_name || `Client ${conversation.client_id}`}
          </h1>
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

        <div className="space-y-4 text-gray-600">
          <p>Platform: {conversation.platform || 'N/A'}</p>
          <div className="flex items-center gap-2">
            <span>Outcome:</span>
            <select
              value={conversation.outcome || ''}
              onChange={(e) => handleOutcomeChange(e.target.value || null)}
              className="border rounded px-2 py-1"
            >
              <option value="">None</option>
              <option value="success">Success</option>
              <option value="failure">Failure</option>
            </select>
          </div>

          <div className="flex gap-2 mt-4">
            <button
              onClick={handleArchiveToggle}
              className="px-4 py-2 bg-gray-100 hover:bg-gray-200 rounded text-gray-700"
            >
              {conversation.archived ? 'Unarchive' : 'Archive'}
            </button>
            <button
              onClick={handleDelete}
              className="px-4 py-2 bg-red-500 hover:bg-red-600 rounded text-white"
            >
              Delete
            </button>
          </div>
        </div>
        <MessageList conversationId={conversation.id} />
      </div>
    </div>
  );
};

export default ConversationDetail;

