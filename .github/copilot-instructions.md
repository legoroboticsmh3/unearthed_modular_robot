This repository controls a modular LEGO Robot using the Pybricks runtime on Spike/Technic hubs.

High-level goal for agents
- Make small, focused code changes that follow the project's configuration-driven patterns.
- Preserve compatibility with Pybricks APIs and the runtime constraints of the hub (limited memory/CPU).

Big-picture architecture (what to read first)
- Entry: `mh_main.py` — creates `Robot(CONFIG)` and starts the async `loader` + `swerve` multitask. Changes here affect program selection and runtime tasks.
- Core robot abstraction: `mh_robot.py` — central Robot class. It imports modular behavior from several files (e.g. `mh_robot_misc`, `mh_swerve_robot_drive`, `mh_robot_remote`, `mh_robot_condition`) — prefer small edits inside these modules or add methods to `Robot` where behavior is cross-cutting.
- Loader/menu: `mh_loader.py` — shows how runs (mission functions) are passed as callables to the loader. Missions follow the pattern: async functions that accept a `robot` instance and use robot APIs.
- Configuration: `mh_config.py` — single source of truth for hardware mapping, PID gains, sensor ports, and feature flags like `hub` and `line.enable`. Edits to numeric constants should ideally be exposed here.
- Missions: `mh_mission_*.py` files — mission scripts are simple scripts or async run functions; some files use high-level DriveBase API directly (e.g., `mh_mission_7.py`). When creating new missions, follow the existing pattern: accept `robot` where appropriate and be callable from `loader`.

Patterns & conventions (project-specific)
- Device mapping via `CONFIG`: Motors, sensors, and directions are mapped in `mh_config.py`. Prefer reading/writing there rather than hard-coding ports.
- Robot composition: `Robot` wires hardware in its constructor, then mixes in behavior via `from mh_x import Y` inside the class. Add new behavior by creating a helper module and importing methods into the `Robot` class in the same style.
- Async multitask pattern: Use `pybricks.tools.multitask` and async `loader`/missions. Missions typically are `async def` and are launched via `multitask` and `run_task(main())` in `mh_main.py`.
- Button handling: UI navigation uses button release detection (compare `pressed` vs `lastPressed`) — copy this pattern if adding button logic.
- Display & speaker: Use `robot.display.number(...)` and `robot.speaker.beep()`/`play_notes(...)` for user feedback; `loader` shows examples.

Dev workflows and runtime notes (how to run/debug)
- This code is written for the Pybricks MicroPython runtime on LEGO hubs. You cannot run the full runtime locally as regular Python. Tests that run on desktop should be isolated from `pybricks` imports.
- Typical development cycle:
  1. Edit `mh_config.py` to set hardware ports/gains.
  2. Copy the modified file to the hub using Pybricks upload tools (or the official `pybricksdev` workflow).
  3. Run the program on the hub. `mh_main.py` is the entrypoint.
- Debugging tips:
  - Use `print(...)` statements; the hub console via Pybricks shows prints.
  - Use `robot.hub.display`, `robot.light`, and `robot.speaker` for in-hardware signals.
  - Avoid heavy logging; the hub has constrained resources.

File-level examples to reference when editing
- Add mission compatible with loader:
  - Look at `mh_mission_02.py` and `mh_run_remote.py` for shapes: async functions that accept `robot` and call `await robot.SwerveStart()` or use `DriveBase` directly.
- Update hardware mapping:
  - `mh_config.py` contains `drive`, `turn`, and `line` sections. Changing port mappings or PID gains belongs here.
- Extend Robot capabilities:
  - Add a module `mh_robot_newfeature.py` with functions and import them into `Robot` exactly as `from mh_robot_misc import ...` is done in `mh_robot.py`.

Integration points & dependencies
- Pybricks runtime (pybricks.*) — Nearly all hardware interfaces are through `pybricks`.
- Local modules: `mh_*` files are the majority of the codebase. Changes to `Robot` method signatures must be reflected across mission files and the loader.

Safe change checklist for agents (mini contract)
- Inputs: small code edits, new mission modules, or config value changes.
- Outputs: compiled change that preserves existing runtimes: `mh_main.py` remains entrypoint, loader accepts run list, Robot constructor must still initialize hardware.
- Error modes: avoid introducing top-level imports of `pybricks` in files that might be imported by desktop tests; keep hardware imports inside functions/classes where possible.

Examples of non-obvious patterns discovered
- Wheel calibration: `mh_robot.py` prints absolute angles and expects manual entry into `CONFIG['turn']['leftZero']` / `rightZero`. Leave prompts and prints intact when modifying init.
- Multitask runner in `mh_main.py`: `await multitask(loader(robot,[run_1]), swerve(robot))` — `loader` and `swerve` are long-running async helpers; don't block them.

What not to change without human review
- Hub selection and stop-button handling in `mh_robot.__init__` (it toggles behavior between `PrimeHub` and `TechnicHub`).
- Motor control limits and calibration constants in `mh_robot.py` and `mh_config.py`.

If anything here is unclear or a section is missing (CI, exact upload commands, or device model variations), tell me which part you'd like expanded and I'll iterate.
