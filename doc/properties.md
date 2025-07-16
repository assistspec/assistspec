1. **Single-Writer-Multiple-Reader (SWMR) Property**:
   - At any given time, a memory block can be in a state where it is writable by only one cache (exclusive state).
   - At any given time, a memory block can be in a state where it is readable by multiple caches (shared state), but not writable by any cache.

2. **Liveness Property**:
   - Every request made by each requester will eventually be processed.