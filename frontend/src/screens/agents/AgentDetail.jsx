import { useDeleteAgent } from "@/services/useAgents"
import { AgentInput } from './AgentInput'

export const AgentDetail = ({ agent, back }) => {
  const deleteAgent = useDeleteAgent()

  return (
    <div className="mt-10">
      <div>
        <button
          className="m-4 bg-gray-700"
          onClick={back}
          disabled={deleteAgent.isPending}
        >
          Back
        </button>
        {agent && <button
          onClick={() => { back(); deleteAgent.mutate(agent.id) }}
          disabled={deleteAgent.isPending}
          className="bg-red-500 text-2xl"
        >
          Delete agent
        </button>}
      </div>
      {!agent && <h2 className="my-2 text-4xl">Add new agent</h2>}
      {agent && <h2 className="my-2">ID: {agent.id}</h2>}
      <AgentInput agent={agent} back={back} />
      <div>
      </div>

    </div>
  )
}
