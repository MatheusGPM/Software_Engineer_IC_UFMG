## 2) Scheduler / deduplicação
- Método: us.codecraft.webmagic.scheduler.DuplicateRemovedScheduler#push(Request request, Task task)
- Arquivo: webmagic-core/src/main/java/us/codecraft/webmagic/scheduler/DuplicateRemovedScheduler.java
- Teste: webmagic-core/src/test/java/us/codecraft/webmagic/scheduler/DuplicateRemovedSchedulerTest.java
- Casos: test_no_duplicate_removed_for_post_request, test_duplicate_removed_for_get_request
