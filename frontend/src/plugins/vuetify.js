// frontend/src/plugins/vuetify.js
import 'vuetify/styles'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import { aliases, mdi } from 'vuetify/iconsets/mdi'
import '@mdi/font/css/materialdesignicons.css'

export default createVuetify({
  components,
  directives,
  icons: {
    defaultSet: 'mdi',
    aliases,
    sets: {
      mdi,
    },
  },
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        dark: false,
        colors: {
          primary: '#4A90E2',
          'primary-darken-1': '#357ABD',
          secondary: '#50E3C2',
          'secondary-darken-1': '#38A89D',
          error: '#D0021B',
          info: '#4A90E2',
          success: '#7ED321',
          warning: '#F5A623',
          background: '#F9F9F9',
          surface: '#FFFFFF',
          'on-background': '#212121',
          'on-surface': '#212121',
        },
      },
      dark: {
        dark: true,
        colors: {
          primary: '#4A90E2',
          'primary-darken-1': '#357ABD',
          secondary: '#50E3C2',
          'secondary-darken-1': '#38A89D',
          error: '#E57373',
          info: '#4A90E2',
          success: '#81C784',
          warning: '#FFB74D',
          background: '#1E1E1E',
          surface: '#2C2C2C',
          'on-background': '#E0E0E0',
          'on-surface': '#E0E0E0',
        },
      },
    },
  },
  defaults: {
    VBtn: {
      borderRadius: '8px',
    },
    VCard: {
      borderRadius: '8px',
    },
    VTextField: {
      borderRadius: '8px',
    },
    VTextarea: {
      borderRadius: '8px',
    },
  },
  typography: {
    fontFamily: 'Inter, sans-serif',
    h1: {
      fontSize: '6rem',
      fontWeight: 300,
      lineHeight: '6rem',
      letterSpacing: '-0.09375em',
    },
    h2: {
      fontSize: '3.75rem',
      fontWeight: 300,
      lineHeight: '3.75rem',
      letterSpacing: '-0.03125em',
    },
    h3: {
      fontSize: '3rem',
      fontWeight: 400,
      lineHeight: '3.125rem',
      letterSpacing: 'normal',
    },
    h4: {
      fontSize: '2.125rem',
      fontWeight: 400,
      lineHeight: '2.5rem',
      letterSpacing: '0.015625em',
    },
    h5: {
      fontSize: '1.5rem',
      fontWeight: 400,
      lineHeight: '2rem',
      letterSpacing: 'normal',
    },
    h6: {
      fontSize: '1.25rem',
      fontWeight: 500,
      lineHeight: '2rem',
      letterSpacing: '0.009375em',
    },
    subtitle1: {
      fontSize: '1rem',
      fontWeight: 400,
      lineHeight: '1.75rem',
      letterSpacing: '0.009375em',
    },
    subtitle2: {
      fontSize: '0.875rem',
      fontWeight: 500,
      lineHeight: '1.375rem',
      letterSpacing: '0.00625em',
    },
    body1: {
      fontSize: '1rem',
      fontWeight: 400,
      lineHeight: '1.5rem',
      letterSpacing: '0.03125em',
    },
    body2: {
      fontSize: '0.875rem',
      fontWeight: 400,
      lineHeight: '1.25rem',
      letterSpacing: '0.015625em',
    },
    button: {
      fontSize: '0.875rem',
      fontWeight: 500,
      lineHeight: '2.25rem',
      letterSpacing: '0.078125em',
      textTransform: 'uppercase',
    },
    caption: {
      fontSize: '0.75rem',
      fontWeight: 400,
      lineHeight: '1.25rem',
      letterSpacing: '0.025em',
    },
    overline: {
      fontSize: '0.75rem',
      fontWeight: 500,
      lineHeight: '2rem',
      letterSpacing: '0.09375em',
      textTransform: 'uppercase',
    },
  },
})
