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
