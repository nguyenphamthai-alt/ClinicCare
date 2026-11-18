export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: false },
  css: [
    '~/assets/css/base.css',
    '~/assets/css/layout.css',
    '~/assets/css/header.css',
    '~/assets/css/components.css',
    '~/assets/css/forms.css',
    '~/assets/css/search.css',
    '~/assets/css/auth.css',
    '~/assets/css/responsive.css'
  ],
  app: {
    head: {
      title: 'ClinicCare Mini EMR',
      meta: [
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'ClinicCare Mini EMR' }
      ]
    }
  },
  runtimeConfig: {
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://localhost:8000'
    }
  }
})
