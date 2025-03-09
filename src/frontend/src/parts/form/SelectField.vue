<template>
    <div class="field">
        <slot name="beforeSelect" v-bind="slotProps"></slot>
        <div ref="triggerElem" class="field fieldSelect" :class="{ multiple, opened }">
            <slot name="fieldInput" v-bind="fieldProps">
                <StringField
                    :readonly="true"
                    :name="name"
                    :disabled="disabled"
                    :title="title"
                    :placeholder="preparedPlaceholder"
                    :value="viewSelected"
                    :class="{ focused: opened }"
                    @click="toggleOpen"
                >
                    <template #afterInput="{ focused }">
                        <i
                            v-if="realValue !== '' && focused && clearbtn"
                            class="icon icon-clear"
                            @mousedown="clear"
                        ></i>
                        <i
                            v-else
                            class="icon icon-arrow-down"
                            @click="!focused ? close() : open()"
                        ></i>
                    </template>
                </StringField>
            </slot>
            <teleport to="body">
                <div
                    ref="movableElem"
                    v-if="!disabled && opened && (!emptyOptions || $slots.beforeValues)"
                    class="field-dropdown innit-position"
                >
                    <slot name="beforeValues" v-bind="optionProps">
                        <SearchField
                            v-if="type === 'search'"
                            ref="search"
                            :value="searchValue"
                            @changeValue="onSearch"
                        />
                    </slot>

                    <div class="field-suggestion-empty">
                        <slot name="info">{{
                            isEmpty(optionList) ? $t('actions.empty_data') : ''
                        }}</slot>
                    </div>
                    <div class="field-suggestions">
                        <div
                            v-for="(val, key) in optionList"
                            :key="key"
                            class="field-suggestion"
                            :class="{
                                selected: isSelected(key, val),
                                hovered: isKeyboardHoveredOptionKey(key, val),
                                disabled: isDisabled(key),
                            }"
                            @mousedown="onChange(key, val)"
                            @mousemove="dropKeyboardHovered"
                        >
                            {{ showValue(val) }}
                        </div>
                    </div>
                </div>
            </teleport>
        </div>
        <slot name="afterSelect" v-bind="slotProps"></slot>
        <slot v-if="afterInputTitle" name="afterInputTitle">
            <span class="afterInputTitle">{{ afterInputTitle }}</span>
        </slot>
    </div>
</template>

<script>
import SelectMixin from './help/SelectMixin'

export default {
    mixins: [SelectMixin],
    data() {
        return {
            opened: false,
            pos: null,
        }
    },
    watch: {
        optionList(newVal, oldVal) {
            if (newVal.length !== oldVal.length) setTimeout(this.setPosition)
        },
    },
    computed: {
        optionProps() {
            return {
                searchValue: this.searchValue,
                isEscAvailable: this.isEscAvailable,
                options: this.optionList,
                onSearch: this.onSearch,
                afterInputTitle: this.afterInputTitle,
            }
        },
        fieldProps() {
            return {
                ...this.optionProps,
                title: this.title,
                open: this.open,
                toggleOpen: this.toggleOpen,
                name: this.name,
                disabled: this.disabled,
                value: this.viewSelected,
                classes: { focused: this.opened },
                placeholder: this.preparedPlaceholder,
                opened: this.opened,
            }
        },
        slotProps() {
            return {
                ...this.fieldProps,
                selected: this.selected,
                realValue: this.realValue,
                onChange: this.onChange,
                unSelect: this.unSelect,
                showValue: this.showValue,
            }
        },
    },
    methods: {
        open() {
            this.opened = true
            this.setPosition()
            this.opened && this.$emit('onOpened')
            this.type === 'search' &&
                setTimeout(() => {
                    this.$refs?.search?.focus()
                }, 100)
            this.parentPageEl.addEventListener('scroll', this.close)
        },
        toggleOpen() {
            if (this.opened) this.close()
            else this.open()
        },
        close() {
            this.opened = false
            this.dropKeyboardHovered()
            this.parentPageEl.removeEventListener('scroll', this.close)
            this.$emit('onClosed')
        },
        changeValue() {
            this.close()
            this.$emit('changeValue', this.realValue, this.name)
        },
        isKeyboardHoveredOptionKey(key, val) {
            if (!this.optionKeys) return false
            val = this.optionKey(key, val)
            const index = this.optionKeys.indexOf(val)
            if (index < 0) return false
            return index === this.pos
        },
        dropKeyboardHovered() {
            this.pos = null
        },
    },
}
</script>
