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
            return this.keyObj?.format
                ? this.keyObj.format(this.row)
                : this.values[this.row[this.keyObj.name]] ?? this.row[this.keyObj.name]
        },
    },
    components: { ValueToString },

    // created()
}
</script>
