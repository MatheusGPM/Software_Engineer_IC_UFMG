# CodigosWEBmagic1 — Como testar 6 métodos do WebMagic com JaCoCo (HTML + XML) e abrir no Edge

Este guia ensina como rodar **cobertura JaCoCo por método**, executando **apenas o teste do desenvolvedor** associado ao método.
O JaCoCo instrumenta o módulo inteiro, mas você consegue “focar” no método ao rodar somente a classe de teste daquele método.

---

## Requisitos

- Git
- Java + Maven
- (Windows) WSL + Microsoft Edge instalado

### Observação sobre versão do Java
Alguns testes com Mockito antigo podem falhar em Java 17+ com erro de *InaccessibleObjectException*.
Se isso ocorrer, use **Java 11** (recomendado) ou aplique `--add-opens` (alternativa).

---

## 1) Baixar o repositório e inicializar submódulos

```bash
git clone https://github.com/MatheusGPM/Software_Engineer_IC_UFMG.git
cd Software_Engineer_IC_UFMG
git submodule update --init --recursive
```

## 2) Entrar no WebMagic original

```bash
cd "07_repos_2026-02-17_(webmagic-orig-e-llm)/webmagic_original"
ls
```

## 3) Rodar JaCoCo para um método (rodando apenas o teste)

```bash
mvn -pl webmagic-core -DskipITs=true -Dtest=NOME_DO_TESTE clean test jacoco:report
```

Relatórios gerados:
- HTML: `webmagic-core/target/site/jacoco/index.html`
- XML:  `webmagic-core/target/site/jacoco/jacoco.xml`

## 4) Abrir o relatório HTML no Edge (Windows + WSL)

```bash
cmd.exe /c start "" msedge "$(wslpath -w "$(realpath webmagic-core/target/site/jacoco/index.html)")"
```

## 5) Copiar XML/HTML para evidências (sem sobrescrever)

```bash
IC="$(realpath ../../..)"
OUT_XML="$IC/02_dados_2026-02-17_(jacoco-e-marcadores)/cobertura_dev_2026-02-17/xml"
OUT_HTML="$IC/02_dados_2026-02-17_(jacoco-e-marcadores)/cobertura_dev_2026-02-17/html"
mkdir -p "$OUT_XML" "$OUT_HTML"

cp "webmagic-core/target/site/jacoco/jacoco.xml" "$OUT_XML/01_UrlUtils_canonicalizeUrl_dev.xml"

DEST="$OUT_HTML/01_UrlUtils_canonicalizeUrl"
rm -rf "$DEST"
mkdir -p "$DEST"
cp -a webmagic-core/target/site/jacoco/. "$DEST/"

cmd.exe /c start "" msedge "$(wslpath -w "$DEST/index.html")"
```

## 6) Lista dos 6 métodos e testes (DEV)

1) UrlUtils#canonicalizeUrl(String, String) — Teste: UrlUtilsTest
2) DuplicateRemovedScheduler#push(Request, Task) — Teste: DuplicateRemovedSchedulerTest
3) HttpUriRequestConverter#convert(Request, Site, Proxy) — Teste: HttpUriRequestConverterTest
4) RegexSelector#select(String) — Teste: RegexSelectorTest
5) SimpleProxyProvider#getProxy(Request, Task) — Teste: SimpleProxyProviderTest
6) FilePipeline#process(ResultItems, Task) — Teste: FilePipelineTest

## 7) Se um teste falhar por Java 17+ (Mockito / InaccessibleObjectException)

### Opção A (recomendado): usar Java 11

```bash
sudo apt update
sudo apt install -y openjdk-11-jdk
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
export PATH="$JAVA_HOME/bin:$PATH"
java -version
```

### Opção B (alternativa): add-opens

```bash
MAVEN_OPTS="--add-opens java.base/java.lang=ALL-UNNAMED" mvn -pl webmagic-core -DskipITs=true -Dtest=DuplicateRemovedSchedulerTest clean test jacoco:report
```
