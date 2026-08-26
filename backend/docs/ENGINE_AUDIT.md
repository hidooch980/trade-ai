# Intelligence module audit

**Date:** 2026-08-26
**Scope:** every `app/*` package whose name contains `intelligence`, `center`,
`_ai`, `_engine`, `network`, `os`, `lab` or `copilot` — 75 packages, 3,401
lines of Python.
**Method:** every file read, then classified with an AST pass that separates
methods containing branching or arithmetic from methods that only append their
argument to a list. Import edges were resolved by grepping the whole tree.

---

## 1. The headline

| Measure | Count |
|---|---|
| Modules audited | 75 |
| Total lines | 3,401 |
| Modules where **no method computes anything** | **67** |
| Modules with at least one method containing logic | 8 |
| Modules imported by anything at all | **0** |
| Modules importing any other `app.` module | **0** |

The 75 packages are not 75 engines. They are, with eight exceptions, the same
class written 67 times with different nouns:

```python
class AI<Noun>Center:
    def __init__(self):
        self.things = []          # four or five empty lists

    def do_something(self, data):
        self.things.append(data)  # every method, verbatim

    def status(self):
        return {"things": len(self.things), "<noun>_engine": "ONLINE"}

<noun> = AI<Noun>Center()
```

`status()` reports `ONLINE` unconditionally. It reports `ONLINE` on a module
that has never been called, because `ONLINE` is a string literal, not a state.

Nothing imports these modules — not `app/api`, not each other, not the tests.
They also import nothing, so they hold no reference to market data, to the
broker, to the database, or to each other. They are disconnected in both
directions.

**Consequence for planning:** "wire up the existing brains" is not a small
task that unlocks value. Wiring all 75 would expose roughly 350 endpoints,
every one of which returns a list length and the word `ONLINE`. The work is
not in the wiring; the logic does not exist yet.

---

## 2. The eight modules that compute something

Ranked by how much of them is logic rather than storage.

| Module | Lines | Logic methods | What it actually does |
|---|---|---|---|
| `market_intelligence` | 112 | 3 / 5 | Three unrelated classes in three files. One averages four scores that are **hardcoded to 50**, so it always returns 50 and always decides `WAIT`. One does keyword sentiment against three positive and three negative English words. One averages a dict of numbers into BUY/SELL/WAIT. |
| `news_intelligence_ai` | 39 | 2 / 2 | Blocks trading when the event name is in a five-item list (NFP, CPI, FOMC, INTEREST_RATE, GDP). Real, if blunt. |
| `risk_center` | 50 | 2 / 3 | Flags accounts whose `drawdown` field is ≥ 10, and an emergency stop that sets a dict key. |
| `security_intelligence` | 59 | 2 / 3 | Scores an auth event: +50 for more than five failed logins, +30 for an unknown device; ≥80 blocks, ≥50 reviews. |
| `compliance_center` | 39 | 1 / 3 | One check: volume above `max_volume` is a violation. |
| `execution_ai` | 38 | 1 / 2 | Rejects a signal when spread or slippage exceeds the signal's own limits, and scores execution quality. The most directly useful thing in the set. |
| `forecast_ai` | 28 | 1 / 1 | Averages technical, sentiment and macro scores into BULLISH / NEUTRAL / BEARISH with a confidence. |
| `global_intelligence` | 123 | 1 / 9 | Two classes in two files. One is a pure stub; the other moves an agent score ±5 on GOOD/BAD. |

Even at the top of this table the logic is a handful of thresholds. None of it
is wrong, but none of it is a system either.

---

## 3. A defect the duplication hides

Six packages define **more than one class across more than one file, and bind
two of them to the same module-level name**:

| Module | Colliding files | Bound name |
|---|---|---|
| `command_center` | `control.py`, `core.py` | `command_center` |
| `global_intelligence` | `engine.py`, `network.py` | `global_intelligence` |
| `market_intelligence` | `fusion.py`, `ai/intelligence_engine.py` | `market_intelligence` |
| `hft_engine` | `core.py`, `engine.py` | `hft_engine` |
| `business_intelligence` | `bi_engine.py`, `core.py` | `bi_engine` / `bi` |
| `macro_intelligence` | two files | — |

Which object `from app.command_center... import command_center` gives you
depends on which file was imported last. That is a real bug waiting for the
first caller, and it is invisible while nothing calls them.

---

## 4. Duplicate families

Same concept, different filename. One member per family is kept; the rest are
removed so nothing later gets built on a doubled foundation.

| Family | Members | Kept | Why |
|---|---|---|---|
| HFT | `hft_engine`, `hft_intelligence`, `hft_intelligence_v2`, `hft_trading_intelligence` | `hft_intelligence` | The only one that is a single coherent class in a single file |
| Compliance | `compliance_center`, `compliance_intelligence`, `compliance_intelligence_center` | `compliance_center` | The only one with a real check |
| Execution | `execution_ai`, `execution_intelligence`, `execution_intelligence_center` | `execution_ai` | The only one with real logic |
| Market | `market_intelligence`, `market_intelligence_center`, `market_intelligence_fusion` | `market_intelligence` | Has logic, and is the module being rebuilt |
| Portfolio | `portfolio_intelligence`, `portfolio_intelligence_center`, `portfolio_optimization_center` | `portfolio_intelligence` | Largest single class |
| Risk | `risk_center`, `risk_intelligence_center` | `risk_center` | Has logic |
| Security | `security_intelligence`, `security_intelligence_center` | `security_intelligence` | Has logic |
| Sentiment | `sentiment_intelligence`, `sentiment_intelligence_v2` | `sentiment_intelligence` | The `_v2` is strictly smaller |
| Operations | `ai_operations_center`, `operations_center` | `operations_center` | Identical; the plain name wins |
| Decision | `decision_intelligence`, `decision_support_center` | `decision_intelligence` | Larger |
| News | `news_intelligence`, `news_intelligence_ai` | `news_intelligence_ai` | Has logic |
| Performance | `performance_intelligence`, `performance_optimization_center` | `performance_intelligence` | Larger |

Nothing imports any member of any family, so removal cannot break a caller.
Verified by grep across `app/` and `tests/` before each deletion.

---

## 5. Recommendation

Building a further "brain" is not what this codebase is short of. It has 75.
What it is short of is logic behind any of them.

The order that repays effort:

1. **Remove the duplicates** (§4) — cheap, and stops the doubled-binding bug
   from reaching a caller. *Done in this change.*
2. **Rebuild one module properly** rather than wiring seventy badly. The
   candidate is `market_intelligence`: fusing several scored inputs into one
   graded decision is genuinely useful, complements the risk brain that
   already exists, and the current version is dead by construction — it
   averages four constants. *Done in this change.*
3. **Leave the remaining stubs where they are** until something needs them.
   Each one is 30 lines; deleting them is easy at any point, and doing it
   without a reason destroys the record of what was intended.

The eight logic-bearing modules in §2 are each worth an hour: `execution_ai`'s
spread and slippage gate and `news_intelligence_ai`'s event blackout both
belong in the trade path next to the risk brain, and neither is far from
usable.
