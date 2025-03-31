import { defineConfig } from 'vitepress'

export default defineConfig({
  title: "inquirer_console",
  description: "优雅的交互式命令行界面工具库",
  lang: 'zh-CN',
  themeConfig: {
    nav: [
      { text: '首页', link: '/' },
      { text: '文章', link: '/articles/inquirer_console_intro' },
      { text: 'GitHub', link: 'https://github.com/Eusen/inquirer_console' }
    ],
    sidebar: {
      '/articles/': [
        {
          text: '文章',
          items: [
            { text: '重磅！Python界最强命令行交互库诞生', link: '/articles/inquirer_console_intro' }
          ]
        }
      ]
    },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/Eusen/inquirer_console' }
    ],
    footer: {
      message: '基于 MIT 许可发布',
      copyright: 'Copyright © 2024-present Eusen'
    }
  }
}) 