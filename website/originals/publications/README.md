# 可供网页导入的合并版 Publications

整理日期：2026-10-27。

## 结果

- Books：3 本。
- Journal Articles：125 篇。
- Conference Articles：120 篇。
- 共 248 条，每类按年份从新到旧、同年按标题排序（未虚构精确发表月日）。
- 247 条具有 DOI；1 条 2011 年 VLSI 会议论文无 DOI，保留 IEEE Xplore 文献 5986130 的原文入口。

## 文件用途

- publications.json：推荐的主数据，保留完整作者/编辑者、来源、原文 URL、DOI 和说明。
- books.json / journal_articles.json / conference_articles.json：分别导入三类栏目。
- ExPub.txt：与目前网站读取路径使用的格式一致；与 publications.bib 内容相同。已用网站现有 parseBibTeX 和分类函数验证解析 248 条、分类数量一致。
- publications.bib：通用 UTF-8 BibTeX，分类为 book/article/inproceedings。为兼容现有简易解析器，展示字段已展开 LaTeX 符号（例如 ±），无嵌套花括号或章节间注释。
- publications.csv：便于 Excel 核对。
- PREVIEW.html：不依赖网络的清单预览，所有条目带原文跳转。
- merge_report.json：逐字段冲突、去重匹配和数量记录。
- excluded_needs_review.json：2 条暂不导入的数据及原因。
- input_manifest.json：输入文件的 SHA-256，便于追溯。

## 合并规则

你提供的 IEEE_Xplore 目录共 232 条（3 本书、111 篇期刊、118 篇会议）。以这些文件的分类、标题、作者、年份、卷期页码为优先。
旧初稿 167 条中，149 条与新文件重合，补入 16 条（14 篇期刊、2 篇会议），另有 2 条移入待核对清单。DOI 去重优先，之后按规范化标题匹配；明确的 ± LaTeX 差异和一条截断标题已合并。期刊扩展版与会议版不同 DOI 时分别保留。
三本书中一本为主编书籍，保留 editor，不伪装为 author。旧初稿提供的来源与 Scholar 链接继续保留。
对缺少 DOI 的补充条目额外查核 Crossref、出版社/作者机构页面。输入 IEEE DOI 按用户提供的导出保留，未逐一在线点击 248 个链接，不声称全部实时可达。

## 暂未纳入网页的两条

1. A 41-mW 30-Gb/s CMOS optical receiver with digitally-tunable cascaded equalization：旧 Scholar 导出有此项，但 Crossref 和 HKUST 作者名单中无 Yan Lu，需你确认；未静默删除，完整记录保留在 excluded_needs_review.json。
   证据：https://researchportal.hkust.edu.hk/en/publications/a-41-mw-30-gbs-cmos-optical-receiver-with-digitally-tunable-casca/
2. Analysis and Design Strategy of On-Chip Charge Pumps for Micro-power Energy Harvesting Applications：书籍章节，不是整本书或期刊/会议论文；独立保留待确认是否增加 Book Chapters。

## 网页导入注意

本次只生成数据包，没有修改网站当前 Publications 内容，也没有上传 GitHub。
主数据已经可用；正式接入网页时，应优先用 JSON 的 url 作为跳转，并在 author 为空时展示 editor 加 “Eds.”。
现有 JS/pub.js 虽能解析全部 BibTeX，但其作者渲染未处理 editor，列表图标也只检查 DOI。因此不能只替换 ExPub.txt 就宣称展示完全正确：正式导入时须补上编辑者展示和无 DOI 时 url 回退（本数据包已包含所需信息）。
本版是已提供资料的合并版，不是 Google Scholar 当前完整账户清单的认证。当前 Scholar 全量在线核对仍受访问限流影响。
