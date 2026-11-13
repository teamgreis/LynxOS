# F-001-K experiment — Observation and control

Run:

```sh
python3 experiments/f001/observation_control_model.py
```

A four-state finite system uses two binary state variables. The partial sensor
observes only the first variable; the full sensor observes both. A partial
actuator changes only the first variable; the full actuator set can change
either variable.

The model checks that:
- the partial sensor cannot distinguish (0,0) from (0,1);
- the partial actuator reaches only two of four states from (0,0);
- the two-actuator set reaches all four states.

Expected final line:

```text
PASS: observation and control assertions satisfied
```

Limitations: finite toy model only; no continuous dynamics, noise, delay,
stability analysis, controller synthesis, security policy, or runtime monitor
is implemented.

## Evidence and limitations

This is an exploratory model, not a production implementation, proof of a real operating-system guarantee, or hardware benchmark. Before citing results, execute this committed artifact itself and record the exact command, tool versions, environment, output, and revision. State the modeled assumptions and omitted cases. Any security claim requires an explicit threat model, negative/adversarial tests, and failure injection. Any performance or efficiency claim requires a credible baseline and repeatable measurements of latency, throughput, CPU, memory, I/O, data movement, and energy where relevant. See the [Engineering Quality Charter](../../docs/foundation/engineering-quality-charter.md).
