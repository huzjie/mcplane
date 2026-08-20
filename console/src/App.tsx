import { useCallback, useState } from "react";
import { McplaneClient } from "@mcplane/sdk";

export default function App() {
  const [baseUrl, setBaseUrl] = useState("http://127.0.0.1:8090");
  const [serverName, setServerName] = useState("echo");
  const [tools, setTools] = useState<{ name: string; description?: string }[]>([]);
  const [result, setResult] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const refresh = useCallback(async () => {
    setBusy(true);
    setError("");
    try {
      const client = new McplaneClient(baseUrl);
      const resp = await client.listTools(serverName);
      const list = (resp.result as { tools?: { name: string; description?: string }[] })?.tools ?? [];
      setTools(list);
    } catch (e) {
      setError(String(e));
    } finally {
      setBusy(false);
    }
  }, [baseUrl, serverName]);

  const callTool = useCallback(
    async (tool: string) => {
      setBusy(true);
      setError("");
      try {
        const client = new McplaneClient(baseUrl);
        const resp = await client.callTool(serverName, tool, {});
        setResult(JSON.stringify(resp.result, null, 2));
      } catch (e) {
        setError(String(e));
      } finally {
        setBusy(false);
      }
    },
    [baseUrl, serverName],
  );

  return (
    <div className="app">
      <h1>mcplane console</h1>
      <p className="subtitle">Stateless MCP control plane</p>

      <div className="controls">
        <input
          value={baseUrl}
          onChange={(e) => setBaseUrl(e.target.value)}
          placeholder="Gateway URL"
          style={{ flex: 1 }}
        />
        <input
          value={serverName}
          onChange={(e) => setServerName(e.target.value)}
          placeholder="Server name"
          style={{ width: 160 }}
        />
        <button onClick={refresh} disabled={busy}>
          {busy ? "Loading..." : "List tools"}
        </button>
      </div>

      {error && <pre style={{ color: "#ff7b72" }}>{error}</pre>}

      <div className="card">
        {tools.length === 0 && !busy && <p style={{ color: "#8b949e" }}>No tools discovered.</p>}
        {tools.map((t) => (
          <div className="tool" key={t.name}>
            <div>
              <div className="tool-name">{t.name}</div>
              <div className="tool-desc">{t.description ?? ""}</div>
            </div>
            <button onClick={() => callTool(t.name)}>Call</button>
          </div>
        ))}
      </div>

      {result && (
        <div className="card">
          <pre>{result}</pre>
        </div>
      )}
    </div>
  );
}
