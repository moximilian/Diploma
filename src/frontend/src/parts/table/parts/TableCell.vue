<template>
    <component
        :is="displayComponent"
        class="table-cell"
        :row="row"
        :keyName="keyObj.name"
        :field="field"
    >
        <slot>{{ viewValue }}</slot>
    </component>
</template>
<script>
import ValueToString from './ValueToString.vue'
export default {
    props: {
        row: { type: Object, default: () => {} },
        keyObj: { type: String, default: () => '' },
        field: { type: Object, default: () => {} },
    },
    data() {
        return {
            values: {
                true: 'Да',
                false: 'Нет',
                null: 'Нет',
            },

            realValue: '',
        }
    },
    computed: {
        displayComponent() {
            return this.field?.displayName ? 'ValueToString' : 'span'
        },
        viewValue() {
            if (!this.row) return
            let value = this.keyObj?.format
                ? this.keyObj.format(this.row, this.row[this.keyObj.name])
                : this.values[this.row[this.keyObj.name]] ?? this.row[this.keyObj.name]
            if (value.length > 64) {
                const toDelete = value.substring(64, value.length)
                value = value.replace(toDelete, '')  + '...'
            }
            return value
        },
    },
    components: { ValueToString },

    // created()
}
</script>
