
## 3) Métodos escolhidos + testes (DEV)

- `UrlUtils#canonicalizeUrl`  
  Teste: `UrlUtilsTest`

- `DuplicateRemovedScheduler#push`  
  Teste: `DuplicateRemovedSchedulerTest` *(pode falhar em Java 17+ por Mockito antigo)*

- `HttpUriRequestConverter#convert`  
  Teste: `HttpUriRequestConverterTest`

- `RegexSelector#select`  
  Teste: `RegexSelectorTest`

- `SimpleProxyProvider#getProxy`  
  Teste: `SimpleProxyProviderTest`

- `FilePipeline#process`  
  Teste: `FilePipelineTest`

## Por que escolhemos esses 6 métodos (bem resumido)

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

