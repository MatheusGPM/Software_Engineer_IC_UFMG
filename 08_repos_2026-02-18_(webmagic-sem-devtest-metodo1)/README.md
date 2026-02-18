# WebMagic — variante sem DEV test do método 1

Esta pasta contém uma variante do WebMagic usada no experimento do IC.

Alteração aplicada:
- Removido o teste do desenvolvedor do método 1 escolhido:
  - Método: UrlUtils#canonicalizeUrl
  - Teste DEV removido: webmagic-core/src/test/java/us/codecraft/webmagic/utils/UrlUtilsTest.java

Objetivo:
- Permitir rodar cobertura (JaCoCo) sem o teste DEV do método 1,
  para comparação posterior com testes gerados por LLM.
