import AppLayout from '@/layout/AppLayout.vue';
import { createRouter, createWebHistory } from 'vue-router';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            component: AppLayout,
            children: [
                {
                    path: '/',
                    name: 'dashboard',
                    component: () => import('@/views/Dashboard.vue')
                },
                {
                    path: '/planes',
                    name: 'planes',
                    component: () => import('@/views/pages/Plane.vue')
                },
                {
                    path: '/people',
                    name: 'people',
                    component: () => import('@/views/pages/People.vue')
                },
                {
                    path: '/flights',
                    name: 'flights',
                    component: () => import('@/views/pages/Flights.vue')
                }
            ]
        }
    ]
});

export default router;
