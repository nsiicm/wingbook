<script setup>
import { ref } from 'vue';

import AppMenuItem from './AppMenuItem.vue';

const model = ref([
    {
        label: 'Home',
        items: [{ label: 'Dashboard', icon: 'pi pi-fw pi-home', to: '/' }]
    },
    {
        label: 'Data',
        items: [
            {
                label: 'Planes',
                icon: 'pi pi-fw pi-plane',
                to: '/planes'
            },
            {
                label: 'People',
                icon: 'pi pi-fw pi-users',
                to: '/people'
            },
            {
                label: 'Flights',
                icon: 'pi pi-fw pi-plane',
                to: '/flights'
            },
            {
                label: 'Accounts',
                icon: 'pi pi-fw pi-user',
                to: '/accounts'
            },
            {
                label: 'Operations',
                icon: 'pi pi-fw pi-briefcase',
                to: '/operations'
            }
        ]
    }
]);
</script>

<template>
    <ul class="layout-menu">
        <template v-for="(item, i) in model" :key="item">
            <app-menu-item v-if="!item.separator" :item="item" :index="i"></app-menu-item>
            <li v-if="item.separator" class="menu-separator"></li>
        </template>
    </ul>
</template>

<style lang="scss" scoped></style>
