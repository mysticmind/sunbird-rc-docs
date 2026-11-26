---
title: "Introduction To Schemas"
---

# Introduction To Schemas

Each registry stores data as entities. The example registry set up via the CLI already has two entity types: `Teacher` and `Student`. View them with:

```bash
$ cat config/schemas/student.json
$ cat config/schemas/teacher.json
```

Or view the samples on [Github](https://github.com/Sunbird-RC/registry-cli/tree/main/src/templates/config/schemas).

| Entity      | Fields                                              | Required                                 |
| ----------- | --------------------------------------------------- | ---------------------------------------- |
| **Teacher** | `name`, `phoneNumber`, `email`, `subject`, `school` | `name`, `phoneNumber`, `email`, `school` |
| **Student** | `name`, `phoneNumber`, `email`, `school`            | all four                                 |

`subject` on a Teacher is one of Math, Hindi, English, History, Geography, Physics, Chemistry, Biology.

::: info
Setting `school` on a Student makes a claim — that the student attends that school — which can be attested by a teacher from the same school.
:::

