# Métodos escolhidos — WebMagic (6)

Objetivo: selecionar 6 métodos do WebMagic que possuem testes feitos pelos desenvolvedores e que sejam tipos diferentes de métodos, para uso no pipeline do projeto.

## Lista dos 6 métodos (com testes)

1) Utilitário / normalização de URL
- Método: us.codecraft.webmagic.utils.UrlUtils#canonicalizeUrl(String url, String refer)
- Arquivo: webmagic-core/src/main/java/us/codecraft/webmagic/utils/UrlUtils.java
- Teste: webmagic-core/src/test/java/us/codecraft/webmagic/utils/UrlUtilsTest.java
- Casos: testFixRelativeUrl, testGetDomain, testGetCharset

2) Scheduler / deduplicação
- Método: us.codecraft.webmagic.scheduler.DuplicateRemovedScheduler#push(Request request, Task task)
- Arquivo: webmagic-core/src/main/java/us/codecraft/webmagic/scheduler/DuplicateRemovedScheduler.java
- Teste: webmagic-core/src/test/java/us/codecraft/webmagic/scheduler/DuplicateRemovedSchedulerTest.java
- Casos: test_no_duplicate_removed_for_post_request, test_duplicate_removed_for_get_request

3) Downloader / conversão HTTP (adapter)
- Método: us.codecraft.webmagic.downloader.HttpUriRequestConverter#convert(Request request, Site site, Proxy proxy)
- Arquivo: webmagic-core/src/main/java/us/codecraft/webmagic/downloader/HttpUriRequestConverter.java
- Teste: webmagic-core/src/test/java/us/codecraft/webmagic/downloader/HttpUriRequestConverterTest.java
- Casos: test_illegal_uri_correct

4) Selector / regex
- Método: us.codecraft.webmagic.selector.RegexSelector#select(String text)
- Arquivo: webmagic-core/src/main/java/us/codecraft/webmagic/selector/RegexSelector.java
- Teste: webmagic-core/src/test/java/us/codecraft/webmagic/selector/RegexSelectorTest.java
- Casos: testRegexWithSingleLeftBracket, testRegexWithLeftBracketQuoted, testRegexWithZeroWidthAssertions

5) Proxy / round-robin provider
- Método: us.codecraft.webmagic.proxy.SimpleProxyProvider#getProxy(Request request, Task task)
- Arquivo: webmagic-core/src/main/java/us/codecraft/webmagic/proxy/SimpleProxyProvider.java
- Teste: webmagic-core/src/test/java/us/codecraft/webmagic/proxy/SimpleProxyProviderTest.java
- Casos: test_get_proxy

6) Pipeline / I-O (arquivo)
- Método: us.codecraft.webmagic.pipeline.FilePipeline#process(ResultItems resultItems, Task task)
- Arquivo: webmagic-core/src/main/java/us/codecraft/webmagic/pipeline/FilePipeline.java
- Teste: webmagic-core/src/test/java/us/codecraft/webmagic/pipeline/FilePipelineTest.java
- Casos: testProcess
