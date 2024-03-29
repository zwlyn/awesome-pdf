import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'             the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [{
        path: '/404',
        component: () => import('@/views/404'),
        hidden: true
    },
    // {
    //     path: '/',
    //     component: Layout,
    //     redirect: '/reportmanage',
    //     children: [{
    //         path: 'reportmanage',
    //         name: 'reportmanage',
    //         component: () => import('@/views/reportmanage/index'),
    //         meta: {
    //             title: '模板管理',
    //             icon: 'reportmanage'
    //         }
    //     }]
    // },
    // {
    //     path: '/datamanage',
    //     component: Layout,
    //     redirect: '/datamanage',
    //     children: [{
    //         path: 'datamanage',
    //         name: 'datamanage',
    //         component: () => import('@/views/datamanage/index'),
    //         meta: {
    //             title: '数据管理',
    //             icon: 'datamanage'
    //         }
    //     }]
    // },
    {
        path: '/reportedit',
        component: Layout,
        redirect: '/reportedit',
        children: [{
            path: 'reportedit',
            name: 'reportedit',
            component: () => import('@/views/reportedit/index'),
            meta: {
                title: 'pdf设计',
                icon: 'reportedit'
            }
        }]
    },
    // {
    //     path: '/pdfrender',
    //     component: Layout,
    //     children: [{
    //         path: 'pdfrender',
    //         name: 'pdfrender',
    //         component: () => import('@/views/pdfrender/index'),
    //         meta: {
    //             title: '报告渲染',
    //             icon: 'pdfrender'
    //         }
    //     }]
    // },
    {
        path: '/',
        component: Layout,
        redirect: '/pdfcombine',
        children: [{
            path: 'pdfcombine',
            name: 'pdfcombine',
            component: () => import('@/views/pdfcombine/index'),
            meta: {
                title: 'pdf合并',
                icon: 'pdfcombine'
            }
        }]
    },
    {
        path: '/pdftotext',
        component: Layout,
        redirect: '/pdftotext',
        children: [{
            path: 'pdftotext',
            name: 'pdftotext',
            component: () => import('@/views/pdftotext/index'),
            meta: {
                title: 'pdf转文本',
                icon: 'pdftotext'
            }
        }]
    },
    // {
    //     path: '/test',
    //     component: Layout,
    //     redirect: '/test',
    //     children: [{
    //         path: 'test',
    //         name: 'test',
    //         component: () => import('@/views/test/index'),
    //         meta: {
    //             title: '测试',
    //             icon: 'test'
    //         }
    //     }]
    // },
    {
        path: '*',
        redirect: '/404',
        hidden: true
    }
]

const createRouter = () => new Router({
    // mode: 'history', // require service support
    scrollBehavior: () => ({
        y: 0
    }),
    routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
    const newRouter = createRouter()
    router.matcher = newRouter.matcher // reset router
}

export default router
