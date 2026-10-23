# LP IDeia

Landing page institucional da IDeia. Página estática em HTML e CSS, sem framework e sem etapa de build: o que está neste repositório é exatamente o que vai para o ar (ADR-001).

- Plano técnico: https://ideia.atlassian.net/wiki/spaces/PI/pages/3637250
- Épico no Jira: https://ideia.atlassian.net/browse/IFI-9
- Design (protótipo v09): Figma `8cGrLRtEjwK6Q3KkjamzSC`

## Estrutura

```
index.html        página única
assets/css/       estilos (tokens do design system em :root)
assets/js/        só se for necessário
assets/img/       WebP e SVG exportados do Figma
assets/fonts/     Manrope variável em WOFF2, subconjunto latino
_headers          cabeçalhos de segurança e cache (Cloudflare Pages)
```

## Rodar localmente

Qualquer servidor estático serve. Com Python, que já vem no macOS e na maioria dos Linux:

```sh
python3 -m http.server 8080
```

Depois abra http://localhost:8080. Abrir o `index.html` direto no navegador funciona para olhar, mas caminhos e cabeçalhos podem se comportar diferente do servidor.

## Validar o HTML

Precisa de Node 22 ou mais novo.

```sh
npm install
npm run validate
```

## Checks do CI

O workflow `.github/workflows/ci.yml` roda em todo pull request e em todo push na `main`, com dois checks:

1. **Validar HTML:** `npm run validate` (html-validate, regras recomendadas).
2. **Verificar links internos:** lychee em modo offline, que confere links e âncoras entre arquivos do próprio site sem acessar a internet.

Para rodar a verificação de links localmente, instale o [lychee](https://lychee.cli.rs) e execute:

```sh
lychee --offline --include-fragments './**/*.html'
```

## Publicar

A publicação é automática pela Cloudflare Pages:

1. Crie uma branch por ticket, por exemplo `ifi-22-estrutura`.
2. Abra um pull request para a `main`. A Cloudflare gera um endereço de preview para o PR, onde se faz o QA.
3. Com os checks verdes e o checklist de revisão marcado no PR, faça o merge. A `main` publica em produção.

Endereço de produção e detalhes do preview: a registrar na T2 (IFI-18).

## Reverter

- **Mais rápido:** no painel da Cloudflare Pages, abra o projeto, vá em Deployments e escolha "Rollback" na publicação anterior.
- **Pelo Git:** reverta o commit ou o merge do PR na `main` (`git revert`), o que publica de novo a versão anterior.
