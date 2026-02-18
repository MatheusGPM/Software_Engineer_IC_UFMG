


# Software_Engineer_IC_UFMG
Repositório do Projeto IC (WebMagic + LLM + JaCoCo).
## Repositories:
- byte-buddy
- commons-io*
- commons-lang*
- google-java-format*
- gson*
- javaparser
- jimfs
- jitwatch
- jsoup*
- zxing

## 3) Métodos escolhidos + testes (DEV)

1) `UrlUtils#canonicalizeUrl`  
- Teste: `UrlUtilsTest`

2) `DuplicateRemovedScheduler#push`  
- Teste: `DuplicateRemovedSchedulerTest` *(pode falhar em Java 17+ por Mockito antigo)*

3) `HttpUriRequestConverter#convert`  
- Teste: `HttpUriRequestConverterTest`

4) `RegexSelector#select`  
- Teste: `RegexSelectorTest`

5) `SimpleProxyProvider#getProxy`  
- Teste: `SimpleProxyProviderTest`

6) `FilePipeline#process`  
- Teste: `FilePipelineTest`

### Por que escolhemos esses 6 métodos (bem resumido)

**Critérios gerais:**
- Têm **testes dos desenvolvedores** (comparação justa com LLM).
- São **tipos diferentes** no WebMagic (utils, scheduler, downloader, selector, proxy, pipeline).
- Cobrem lógicas variadas (URL/string, deduplicação, conversão HTTP, regex, escolha de proxy, I/O).

**Motivos por método:**
- URL utilitária e determinística  
- Deduplicação (regras GET vs POST)  
- Adapter/conversão para HTTP  
- Extração por regex  
- Seleção/rotação de proxy  
- Pipeline com escrita (I/O)

