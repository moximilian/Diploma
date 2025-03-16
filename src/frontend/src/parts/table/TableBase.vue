<template>
    <div class="table-base-container">
        <slot name="before"></slot>
        <div class="table-base-body">
            <div class="table-base-header table-base-row">
                <div v-for="key of keys" :key="key" class="table-cell">
                    {{ titles[key.name] }}
                </div>
            </div>
            <TableRow v-for="row, index in rows" :key="row.id" :row="row" :class="{even: index%2!=0}">
                <div v-for="key of keys" :key="key.name" class="table-cell">
                    {{ values[row[key.name]] ?? row[key.name] }}
                </div>
            </TableRow>
        </div>
    </div>
</template>
<script>
import TableRow from './parts/TableRow.vue'
import displayRules from '@/core/displayRules'
export default {
    props: {
        keys: { type: Array, default: () => [] },
        rows: { type: Array, default: () => [] },
        displayName: { type: String, default: () => '' },
    },
    data() {
        return {
            titles: {},
            values: {
                'true': 'Да',
                'false': 'Нет'
            }
        }
    },
    methods: {
        getAllNames() {
            const display = displayRules[this.displayName + 'Display']
            this.titles = display.reduce((titles, field) => {
                titles[field.props.name] = field.props.title
                return titles
            }, {})
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
