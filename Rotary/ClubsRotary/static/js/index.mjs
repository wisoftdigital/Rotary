import { UrlBuilder } from "markmap-common";
import { buildTree } from "markmap-html-parser";
import MarkdownIt from "markdown-it";
import md_ins from "markdown-it-ins";
import md_mark from "markdown-it-mark";
import md_sub from "markdown-it-sub";
import md_sup from "markdown-it-sup";
import { plugins, createTransformHooks } from "./plugins.mjs";
import "yaml";
import "highlight.js";
import "@iktakahiro/markdown-it-katex";
function initializeMarkdownIt() {
  const md = MarkdownIt({
    html: true,
    breaks: true
  });
  md.use(md_ins).use(md_mark).use(md_sub).use(md_sup);
  return md;
}
function patchJSItem(urlBuilder, item) {
  if (item.type === "script" && item.data.src) {
    return {
      ...item,
      data: {
        ...item.data,
        src: urlBuilder.getFullUrl(item.data.src)
      }
    };
  }
  return item;
}
function patchCSSItem(urlBuilder, item) {
  if (item.type === "stylesheet" && item.data.href) {
    return {
      ...item,
      data: {
        ...item.data,
        href: urlBuilder.getFullUrl(item.data.href)
      }
    };
  }
  return item;
}
const builtInPlugins = plugins;
function cleanNode(node) {
  while (!node.content && node.children.length === 1) {
    node = node.children[0];
  }
  while (node.children.length === 1 && !node.children[0].content) {
    node = {
      ...node,
      children: node.children[0].children
    };
  }
  return {
    ...node,
    children: node.children.map(cleanNode)
  };
}
class Transformer {
  constructor(plugins2 = builtInPlugins) {
    this.assetsMap = {};
    this.urlBuilder = new UrlBuilder();
    this.hooks = createTransformHooks(this);
    this.plugins = plugins2.map(
      (plugin) => typeof plugin === "function" ? plugin() : plugin
    );
    const assetsMap = {};
    for (const { name, transform } of this.plugins) {
      assetsMap[name] = transform(this.hooks);
    }
    this.assetsMap = assetsMap;
    const md = initializeMarkdownIt();
    this.md = md;
    this.hooks.parser.call(md);
  }
  transform(content, fallbackParserOptions) {
    var _a;
    const context = {
      content,
      features: {},
      contentLineOffset: 0,
      parserOptions: fallbackParserOptions
    };
    this.hooks.beforeParse.call(this.md, context);
    const html = this.md.render(context.content, {});
    this.hooks.afterParse.call(this.md, context);
    const root = cleanNode(buildTree(html, context.parserOptions));
    root.content || (root.content = `${((_a = context.frontmatter) == null ? void 0 : _a.title) || ""}`);
    return { ...context, root };
  }
  /**
   * Get all assets from enabled plugins or filter them by plugin names as keys.
   */
  getAssets(keys) {
    const styles = [];
    const scripts = [];
    keys ?? (keys = this.plugins.map((plugin) => plugin.name));
    for (const assets of keys.map((key) => this.assetsMap[key])) {
      if (assets) {
        if (assets.styles)
          styles.push(...assets.styles);
        if (assets.scripts)
          scripts.push(...assets.scripts);
      }
    }
    return {
      styles: styles.map((item) => patchCSSItem(this.urlBuilder, item)),
      scripts: scripts.map((item) => patchJSItem(this.urlBuilder, item))
    };
  }
  /**
   * Get used assets by features object returned by `transform`.
   */
  getUsedAssets(features) {
    const keys = this.plugins.map((plugin) => plugin.name).filter((name) => features[name]);
    return this.getAssets(keys);
  }
}
const transformerVersions = {
  "markmap-lib": "0.17.2"
};
export {
  Transformer,
  builtInPlugins,
  transformerVersions
};