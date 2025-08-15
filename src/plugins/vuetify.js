// Styles
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

// Composables
import { createVuetify } from 'vuetify'
import { VApp } from 'vuetify/components/VApp';
import { VAppBar, VAppBarNavIcon, VAppBarTitle } from 'vuetify/components/VAppBar';
import { VAvatar } from 'vuetify/components/VAvatar';
import { VBtn } from 'vuetify/components/VBtn';
import { VCard, VCardActions, VCardText, VCardTitle, VCardSubtitle, VCardItem } from 'vuetify/components/VCard';
import { VCol, VContainer, VRow, VSpacer } from 'vuetify/components/VGrid';
import { VDialog } from 'vuetify/components/VDialog';
import { VDivider } from 'vuetify/components/VDivider';
import { VExpansionPanel, VExpansionPanelText, VExpansionPanelTitle, VExpansionPanels } from 'vuetify/components/VExpansionPanel';
import { VIcon } from 'vuetify/components/VIcon';
import { VImg } from 'vuetify/components/VImg';
import { VList, VListItem, VListItemTitle, VListItemSubtitle, VListSubheader, VListItemAction, VListItemMedia } from 'vuetify/components/VList';
import { VMain } from 'vuetify/components/VMain';
import { VMenu } from 'vuetify/components/VMenu';
import { VNavigationDrawer } from 'vuetify/components/VNavigationDrawer';
import { VOverlay } from 'vuetify/components/VOverlay';
import { VProgressCircular } from 'vuetify/components/VProgressCircular';
import { VSelect } from 'vuetify/components/VSelect';
import { VSnackbar } from 'vuetify/components/VSnackbar';
import { VSwitch } from 'vuetify/components/VSwitch';
import { VTab, VTabs } from 'vuetify/components/VTabs';
import { VTextarea } from 'vuetify/components/VTextarea';
import { VTextField } from 'vuetify/components/VTextField';
import { VToolbarTitle } from 'vuetify/components/VToolbar';
import { VWindow, VWindowItem } from 'vuetify/components/VWindow';
import { themes } from '@/themes';

export default createVuetify({
  components: {
    VApp,
    VAppBar,
    VAppBarNavIcon,
    VAppBarTitle,
    VAvatar,
    VBtn,
    VCard,
    VCardActions,
    VCardText,
    VCardTitle,
    VCardSubtitle,
    VCardItem,
    VCol,
    VContainer,
    VDialog,
    VDivider,
    VExpansionPanel,
    VExpansionPanelText,
    VExpansionPanelTitle,
    VExpansionPanels,
    VIcon,
    VImg,
    VList,
    VListItem,
    VListItemTitle,
    VListItemSubtitle,
    VListSubheader,
    VListItemAction,
    VListItemMedia,
    VMain,
    VMenu,
    VNavigationDrawer,
    VOverlay,
    VProgressCircular,
    VRow,
    VSelect,
    VSnackbar,
    VSpacer,
    VSwitch,
    VTab,
    VTabs,
    VTextarea,
    VTextField,
    VToolbarTitle,
    VWindow,
    VWindowItem,
  },
  theme: {
    defaultTheme: 'dark',
    themes,
  },
});
