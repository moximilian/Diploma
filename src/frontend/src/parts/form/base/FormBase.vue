<template>
    <div class="form-container">
        <div class="form">
            <slot name="form-top"> </slot>
            <div class="label-type-field" v-for="(field, index) of displayRule" :key="index">
                <component
                    :is="displayComponent(field)"
                    v-if="canModify"
                    v-bind="field.props"
                    @changeValue="onChangeValue"
                >
                    <template #beforeInput>
                        <span>{{ field.props.title }}</span>
                    </template>
                </component>
                <ShowValueField v-else v-bind="field.props" />
            </div>
            <div class="form-bottom" id="form-bottom">
                <slot name="form-bottom" :entity="entity"> </slot>
            </div>
        </div>
    </div>
</template>
<script>
import displayRules from '@/core/displayRules'
export default {
    props: {
        displayName: { type: String, default: () => '' },
        defaults: { type: Object, default: null },
        canModify: { type: Boolean, default: () => false },
    },
    data() {
        return {
            entity: {},

            unchangedEntity: {},
            displayRules: structuredClone(displayRules),
            sameValidationForm: true,
            requiredForm: true,

            displayRule: null,
        }
    },
    computed: {
        displayNameR() {
            return this.displayName + 'Display'
        },
        fieldset() {
            return this.displayRules?.[this.displayNameR] ?? null
        },
        action() {
            return this.$route?.params?.action
        },
        isNew() {
            return this.action === 'new'
        },
        entityId() {
            return this.$route.params?.id ?? null
        },
    },
    watch: {
        displayRule() {
            this.displayRule.map(rule => {
                const key = rule.props.name
                this.entity[key] = this.unchangedEntity[key] ?? rule.props.value
            })
        },
    },
    methods: {
        getDisplayRule(cb) {
            this.displayRule = this.injectWithValues(this.fieldset)
            cb?.()
        },
        injectWithValues(fields) {
            fields.map(field => {
                const defaultValue = this.defaults
                    ? this.defaults[field.props.name]
                    : field.props.value
                ![null, undefined].includes(field.displayName)
                    ? this.getFieldValue(field, defaultValue, finalValue => {
                          if (!this.unchangedEntity[field.props.name])
                              this.unchangedEntity[field.props.name] = field.props.value
                          field.props.value = finalValue
                      })
                    : (field.props.value = defaultValue)
            })
            return fields
        },
        getFieldValue(field, defaultValue, cb) {
            if (!defaultValue) return ''
            this.$api[field.displayName].one({ [field.fieldKey ?? 'id']: defaultValue }, res => {
                if (res.detail) return defaultValue
                cb?.(
                    Array.isArray(field.showName)
                        ? field.showName.map(field => res[field]).join(' ')
                        : res[field.showName]
                )
            })
        },
        componentProps(field) {
            return { ...field.props }
        },

        displayComponent(field) {
            return field.display
        },
        onChangeValue(value, name) {
            this.entity[name] = value
        },
    },
    created() {
        this.getDisplayRule(() => {
            this.displayRule.map(rule => {
                const key = rule.props.name
                this.entity[key] = rule.props.value
            })
        })
    },
}
</script>
