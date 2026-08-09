import React from "react";
import { createRoot } from "react-dom/client";
import "./style.css";
import { useEffect, useState } from "react";

function App() {
  const [health,setHealth]=useState("CHECKING");
  const [positions,setPositions]=useState<any[]>([]);
  const [dashboard,setDashboard]=useState<any>(null);
  const [market,setMarket]=useState<any>(null);
  const [error,setError]=useState("");

  useEffect(()=>{
    const load=async()=>{
      try{
        const [h,d,m,p]=await Promise.all([
          fetch("/health"),
          fetch("/dashboard/status"),
          fetch("/market/status"),
          fetch("/api/trading/positions")
        ]);
        if(!h.ok) throw new Error("Health API failed");
        setHealth("ONLINE");
        if(d.ok) setDashboard(await d.json());
        if(m.ok) setMarket(await m.json());
        if(p.ok){
          const x=await p.json();
          setPositions(Array.isArray(x)?x:(x.positions||[]));
        }
        setError("");
      }catch(e){setHealth("OFFLINE");setError(String(e))}
    };
    load();
    const t=setInterval(load,5000);
    return()=>clearInterval(t);
  },[]);

  const pos=positions[0]||{};
  const pnl=Number(pos.pnl??pos.profit??0);
  const symbol=pos.symbol||"NO OPEN POSITION";
  const side=pos.side||pos.type||"—";

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="logo">TRADE<span>AI</span></div>
        <nav>
          {["Dashboard","Positions","Market","AI Brain","Risk","Trades","System"].map((x,i)=>
            <div className={"nav "+(i===0?"active":"")} key={x}>{x}</div>
          )}
        </nav>
      </aside>

      <main className="main">
        <header>
          <div>
            <h1>Trading Dashboard</h1>
            <p>Trade-AI Control Center</p>
          </div>
          <div className="status">
            <span></span>{health==="ONLINE"?"SYSTEM ONLINE":"SYSTEM OFFLINE"}
          </div>
        </header>

        {error&&<div className="panel error">{error}</div>}

        <section className="cards">
          <div className="card"><label>BALANCE</label><strong>{dashboard?.balance??"—"}</strong></div>
          <div className="card"><label>EQUITY</label><strong>{dashboard?.equity??"—"}</strong></div>
          <div className="card"><label>OPEN POSITIONS</label><strong>{positions.length}</strong></div>
          <div className="card"><label>FLOATING PNL</label><strong className={pnl>=0?"profit":"loss"}>{pnl>=0?"+":""}{pnl}</strong></div>
        </section>

        <section className="grid">
          <div className="panel">
            <div className="panel-title">LIVE POSITION</div>
            {positions.length?
              <div className="position">
                <div><small>{symbol}</small><h2>{side}</h2></div>
                <div><small>VOLUME</small><b>{pos.volume??"—"}</b></div>
                <div><small>ENTRY</small><b>{pos.entry_price??pos.entry??"—"}</b></div>
                <div><small>CURRENT</small><b>{pos.current_price??pos.price??"—"}</b></div>
                <div><small>PNL</small><b className={pnl>=0?"profit":"loss"}>{pnl}</b></div>
              </div>
              :<div className="empty">NO OPEN POSITIONS</div>
            }
          </div>

          <div className="panel">
            <div className="panel-title">MARKET STATUS</div>
            <div className="decision">
              <div className="decision-value">{market?.status||market?.decision||"LIVE"}</div>
              <div className="confidence">{market?.symbol||"Market API connected"}</div>
            </div>
          </div>
        </section>

        <section className="panel">
          <div className="panel-title">SYSTEM COMPONENTS</div>
          <div className="systems">
            {["API","MT5 Bridge","Position Store","Position Monitor","Market Runner","Risk Manager"].map(x=>
              <div key={x}><span className="ok"></span>{x}</div>
            )}
          </div>
        </section>
      </main>
    </div>
  );
}

createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
