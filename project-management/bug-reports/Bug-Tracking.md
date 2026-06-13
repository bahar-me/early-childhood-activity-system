# Bug Tracking Log

This document records the main bugs identified during the development and testing process of the Early Childhood Activity Recommendation System. Each bug entry includes the related sprint, module, issue type, severity, priority, detection date, resolution date, and final status.

| Bug ID | Sprint | Test Case ID | Module                | Bug Type      | Description                                                      | Severity | Priority | Status   | Detection Date | Resolution Date | Notes                                           |
| ------ | -----: | ------------ | --------------------- | ------------- | ---------------------------------------------------------------- | -------- | -------- | -------- | -------------- | --------------- | ----------------------------------------------- |
| BR-01  |      2 | TC-04-01     | Recommendation Engine | Functional    | Age group filtering was not applied in activity recommendations. | Medium   | High     | Resolved | 20.05.2026     | 21.05.2026      | Recommendation filtering logic was improved.    |
| BR-02  |      3 | TC-01-02     | Authentication        | Validation    | Invalid login credentials were not handled clearly.              | Low      | Medium   | Resolved | 11.06.2026     | 12.06.2026      | Authentication response messages were improved. |
| BR-03  |      3 | TC-05-02     | Activity List         | UI            | Empty activity result message was not informative.               | Low      | Low      | Resolved | 17.05.2026     | 17.05.2026      | User feedback message was improved.             |
| BR-04  |      4 | TC-03-02     | School Management     | Functional    | School update changes were not saved to the database.            | High     | High     | Resolved | 02.02.2026     | 03.02.2026      | Missing database commit was fixed.              |
| BR-05  |      5 | TC-04-01     | Authentication        | Security      | Expired JWT token was not handled correctly.                     | Medium   | High     | Resolved | 11.06.2026     | 12.06.2026      | Centralized 401 handling was added.             |
| BR-06  |      6 | TC-04-03     | Gemini Integration    | Configuration | Gemini dependency installation failed in the CI pipeline.        | Medium   | Medium   | Resolved | 25.05.2026     | 26.05.2026      | CI dependency configuration was corrected.      |
| BR-07  |      7 | TC-05-04     | Activity Management   | Functional    | Activity planning fields were not preserved during update.       | Medium   | Medium   | Resolved | 27.05.2026     | 27.05.2026      | Extended planning field support was added.      |
| BR-08  |      7 | TC-06-02     | AI Adaptation         | Functional    | Adapted activities were difficult to identify after saving.      | Medium   | Medium   | Resolved | 23.05.2026     | 24.05.2026      | Activity traceability was improved.             |
| BR-09  |      8 | TC-07-01     | Mobile Integration    | Configuration | Android application could not connect to the local backend.      | Medium   | Medium   | Resolved | 27.03.2026     | 29.03.2026      | Capacitor network configuration was updated.    |

## Summary

During the project development process, bugs were mainly observed in authentication, recommendation logic, AI integration, activity management, school management, and mobile integration modules. Most issues were resolved by improving validation logic, API handling, database transaction flow, CI configuration, and mobile network settings.

The bug tracking process helped improve the stability, usability, and reliability of the system before final delivery.
