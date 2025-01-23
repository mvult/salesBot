import { useState } from 'react'
// import './App.css'
import { AgentList } from './screens/agents'
import { ConversationList } from './screens/conversations'


const App = () => {
  const [activeTab, setActiveTab] = useState('agents'); // State to track the active tab

  return (
    <main className="flex min-h-screen flex-col items-center justify-top mt-8">
      <div className="w-full max-w-7xl px-4">
        <div className="w-full border-b">
          <button
            onClick={() => setActiveTab('agents')}
            className={`px-4 py-2 mx-2 text-sm font-medium ${activeTab === 'agents'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-500 hover:text-gray-700'
              }`}
          >
            Agents
          </button>
          <button
            onClick={() => setActiveTab('conversations')}
            className={`px-4 py-2 mx-2 text-sm font-medium ${activeTab === 'conversations'
              ? 'text-blue-600 border-b-2 border-blue-600'
              : 'text-gray-500 hover:text-gray-700'
              }`}
          >
            Conversations
          </button>
        </div>

        {/* Tab Content */}
        <div className="mt-4">
          {activeTab === 'agents' && <AgentList />}
          {activeTab === 'conversations' && <ConversationList />}
        </div>
      </div>
    </main>
  );
};


export default App
