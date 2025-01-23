import { useDeleteAgent } from "@services/useAgents"

export const AgentDetail = ({ agent }) => {
  const deleteAgent = useDeleteAgent()

  return (
    <div>
      <h2>{agent.name}</h2>
      <button
        onClick={() => deleteAgent(agent.id)}
        disabled={deleteAgent.isPending}
      >Delete agent</button>
    </div>
  )
}
