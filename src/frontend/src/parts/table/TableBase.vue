<template>
    <div class="table-base-container">
        <slot name="before"></slot>
        <div class="table-base-body">
            <div class="table-base-header table-base-row">
                <div v-for="key of keys" :key="key" class="table-cell flex-container-row">
                    {{ titles?.[key?.name] || key?.title || '' }}
                    <BaseBtn
                        class="small"
                        :outline="true"
                        v-if="key?.isCustom"
                        @click="$emit('onCustomKeyDelete', key.name, rows)"
                        >-</BaseBtn
                    > 
                    <!-- @TODO Переделать эту кнопку в слот -->
                </div>
                <slot name="custom-title-key" :rows="rows"></slot>
            </div>
            <div v-if="rows.length > 0">
                <TableRow
                    v-for="(row, index) in rows"
                    :key="row.id"
                    :row="row"
                    :isClickable="isClickable"
                    :class="{ even: index % 2 != 0 }"
                    @clickRow.self="changeAction"
                >
                    <slot name="first-item" :row="row"></slot>
                    <div v-for="key of tableKeys" :key="key?.name" class="table-cell">
                        <div v-if="key?.name">
                            <TableCell :row="row" :keyObj="key" :field="getField(key.name)">
                                <slot
                                    name="table-cell"
                                    :row="row"
                                    :keyObj="key"
                                    :field="getField(key.name)"
                                >
                                </slot>
                            </TableCell>
                        </div>
                    </div>
                    <slot name="last-item" :row="row"></slot>
                </TableRow>
            </div>
            <div v-else>Нет данных</div>
        </div>
    </div>
</template>
<script>
import TableRow from './parts/TableRow.vue'

import displayRules from '@/core/displayRules'
export default {
    emits: ['onCustomKeyDelete'],
    props: {
        keys: { type: Array, default: () => [] },
        rows: { type: Array, default: () => [] },
        displayName: { type: String, default: () => '' },
        isClickable: { type: Boolean, default: () => true },
    },
    data() {
        return {
            titles: {},
            displayRules: null,
            fields: [],
        }
    },
    computed: {
        tableKeys() {
            return this.keys.filter(key => key.name !== 'slot')
        },
    },
    methods: {
        getField(key) {
            return this.fields.find(field => field.props.name === key)
        },
        getAllNames() {
            this.fields = displayRules[this.displayName + 'Display']
            this.titles = this.fields.reduce((titles, field) => {
                titles[field.props.name] = field.props.title
                return titles
            }, {})
        },
        changeAction(row) {
            if (!this.isClickable) return
            const fullPath = this.$route.path
            const source = fullPath.split('/')[1]
            this.$router.push(`/${source}/show/${row.id}`)
        },
    },
    created() {
        this.getAllNames()
    },
    components: {
        TableRow,
    },
}
</script>
