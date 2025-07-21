# Handling API Breaking Changes – Answers

## 1. What Is a Breaking Change?

Any update made to an API that has the potential of breaking the current client applications, cause them to act improperly, or necessitate code changes to shift compatibility is considered a breaking change.  Because breaking changes can affect user experience, interrupt live services, and necessitate immediate fixes for numerous clients, they are particularly important in real-world production systems.  Breaking updates usually result in a non-backward compatible change to the sync between the API and its users.

**Examples of breaking changes for the Weather API:**

1. **Renaming or Removing Fields:**
   - Changing the field name from `temperature` to `temp`, or removing the `condition` field entirely. Clients expecting the original field names will fail to parse the response or display incomplete data.
   - _Example:_
     ```json
     // Old approach:
     { "hour": 0, "temperature": "18", "condition": "Clear" }
     // New (breaking):
     { "hour": 0, "temp": "18" }
     ```

2. **Changing Data Types:**
   - Modifying the type of a field, such as changing `temperature` from a string to a number, or from Celsius to Fahrenheit without clear indication. This can break parsing logic or cause incorrect calculations in the frontend.
   - _Example:_
     ```json
     // Old approach:
     { "temperature": "18" }
     // New (breaking):
     { "temperature": 18 }
     ```

3. **Altering the Structure of the Response:**
   - Wrapping the `Weather` array in an additional object, or changing the array to an object keyed by hour. This breaks clients that expect a flat array.
   - _Example:_
     ```json
     // Old approach:
     { "Weather": [ ... ] }
     // New (breaking):
     { "data": { "Weather": [ ... ] } }
     ```

4. **Removing or Reordering Array Elements:**
   - If clients rely on the array having 24 elements (one per hour), returning fewer elements or changing the order can break UI logic or analytics.

5. **Changing Field Semantics Without Notice:**
   - For instance, changing the meaning of `condition` from a string description ("Clear") to a numeric code (1 = Clear, 2 = Cloudy, etc.) without documentation or versioning.

I have been there, in my experience even though it seems like a minor change, like renaming a table field, it can cause widespread issues if not communicated and coordinated properly. I once saw a production MVP dashboard go blank for hundreds of users because one of our backend engineering team member renamed a table field without notifying the two frontend guys in the team. This actually led everyone of us to implement git-slack notification with proper commit message for PR or any change whatsoever. It is a lesson learnt that there should be no gap in communication channels between teams especially when the team is working async. In real-time systems, it’s essential to treat every change with caution and also involve all stakeholders in the process so that everyone can be in the loop. 


## 2. Coordinating Across Multiple Frontends

Managing API schema changes when multiple frontend clients update at different rates is a common challenge in real-world production environments. In my experience, the safest approach is to use versioning and backward compatibility to ensure that no client is forced to update immediately. For instance, when we needed to introduce a new required field to our API, we released a new version (such as tag release, /v2/) while keeping the old version (/v1/) available for clients that hadn’t updated yet. This allowed frontend teams with different release cycles to migrate at their own pace, reducing the risk of outages. Beyond API management I have adopted this extensively and in fact there is a framework I built in GO which I often use tag release to push up.

Some practical strategies I’ve used include:
- **API Versioning:** Maintain multiple API versions (like /v1/, /v2/) so older clients continue to function while newer clients adopt the changes. Clearly communicate deprecation timelines well in advance.
- **Deprecation Notices:** Add warnings in API responses or documentation to alert clients about upcoming changes and encourage migration.
- **Feature Flags and Conditional Logic:** Sometimes, we introduce new fields or behaviors behind feature flags, allowing specific clients to opt-in before making the change default.
- **Comprehensive Documentation:** Keep changelogs and migration guides up to date, so frontend teams know exactly what’s changing and how to adapt.
- **Regular Syncs and Communication:** Schedule regular meetings or async updates ( either via Slack or email) with all client teams to discuss upcoming changes and gather feedback. Just like the way we usually jump on call during sprint planning.

A lesson I learned is that even with good documentation, some clients may lag behind. In one project, we set a hard cutoff date for an old API version, but a key client missed the communication and their app broke in production. Since then, I always make sure to over-communicate, provide clear migration paths, and monitor usage of deprecated endpoints before final removal. This approach minimizes disruption and keeps all teams aligned. 


## 3. How to Catch Breaking Changes During Development

Catching breaking changes early is very very important for maintaining stability in production systems. In my experience, the most effective way to detect breaking changes is to integrate automated API layer testing and schema validation into the development workflow. For instance, in one of my previous teams, we used tools like Swagger/OpenAPI to define our API layers, and set up CI pipelines that would automatically run layer tests whenever a pull request was opened. If a proposed change broke the API layer, the build would fail and the team would be notified immediately.

Some practical steps I’ve found valuable:
- **Automated Contract Testing:** Use tools like Swagger/OpenAPI, Postman, or Pact to define and validate API schemas. Integrate these tests into CI/CD pipelines so that any breaking change is caught before merging.
- **Consumer-Driven Contract Tests:** Encourage frontend teams to contribute tests that reflect their expectations of the API. This way, backend changes are validated against real client usage.
- **Schema Validation and Linting:** Use schema validation libraries to enforce response structure and data types during development and testing.
- **Code Reviews and Pair Programming:** It makes every sense to make it a habit to review API changes with both backend and frontend engineers present, so potential breaking changes are discussed earlier within the engineering team.
- **Staging Environments:** Deploy changes to a staging environment where all clients can run integration tests before production rollout.

My experience within 7years: We once missed a breaking change because a developer updated the API response but forgot to update the OpenAPI spec. The frontend team only discovered the issue after deployment, causing a scramble to hotfix. Since then, we made it mandatory to update and validate the API spec as part of every pull request, and breaking changes have been caught much earlier. This process has saved us from several potential incidents. We often call it all hands on desk with asynchronous promotion.


## 4. Policy for Releasing Changes

In my previous teams, we established a clear and disciplined policy for managing API schema changes to ensure safety and minimize disruption. The core principle was that no breaking change should ever reach production without thorough review in fact for you to merge a PR three Engineers must review the PR, communication, and a migration plan. We formalized this with a documented process that every engineer was expected to follow.

Key elements of our policy included:
- **Change Proposals and Design Reviews:** Any schema change, especially breaking ones required a written proposal and a design review meeting with both backend and frontend leads. This ensured all stakeholders understood the impact and could raise concerns early.
- **Deprecation and Sunset Policy:** We always introduced breaking changes in stages: first, mark fields or endpoints as deprecated, then communicate a sunset date (often 3–6 months out), and only remove them after all clients had migrated.
- **Versioning:** All breaking changes were released under a new API version. We never made breaking changes to existing versions in production.
- **Automated Testing and Validation:** CI/CD pipelines enforced contract tests and schema validation for every pull request. No change could be merged without passing these checks.
- **Comprehensive Documentation:** Every change was documented in a changelog and communicated via Slack, email, and internal wikis. We also provided migration guides for client teams.
- **Release Coordination:** Major changes were coordinated with release managers and product owners to ensure proper rollout and monitoring.

Early in my career while working for Lidya Finance a fintech company, we once pushed a breaking change without a formal deprecation process, assuming all clients would update quickly. One client didn’t, and their service broke, leading to a loss of trust I attributed this to being novice at that time. Since then, I’ve always insisted on a formal deprecation and communication process, and it’s paid off—no more surprises for clients, and much smoother releases overall.