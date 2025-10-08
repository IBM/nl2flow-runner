(define (domain basic_test-domain)
    (:requirements :action-costs :typing :equality)
    (:types
        generic - object
        operator - object
        has-done-state - object
        constraint-status - object
        datum-state - object
        num-retries - object
        object
    )

    (:constants
        False True - constraint-status
        certain uncertain unknown - datum-state
        database_link list_of_errors new_object_generic_0 - generic
        future past present - has-done-state
        try_level_0 try_level_1 try_level_2 try_level_3 try_level_4 try_level_5 try_level_6 - num-retries
        find_errors fix_errors - operator
    )

    (:predicates
        (has_done ?x1 - operator ?x2 - has-done-state)
        (been_used ?x1 - generic)
        (new_item ?x1 - generic)
        (known ?x1 - generic ?x2 - datum-state)
        (not_slotfillable ?x1 - generic)
        (is_mappable ?x1 - generic ?x2 - generic)
        (not_mappable ?x1 - generic ?x2 - generic)
        (mapped ?x1 - generic)
        (not_usable ?x1 - generic)
        (mapped_to ?x1 - generic ?x2 - generic)
        (connected ?x1 - operator ?x2 - num-retries ?x3 - num-retries)
        (free ?x1 - generic)
        (done_goal_pre)
        (done_goal_post)
        (has_done_find_errors ?x1 - generic ?x2 - num-retries)
        (has_done_fix_errors ?x1 - generic ?x2 - num-retries)
    )

    (:functions
        (total-cost) - number
        (slot_goodness ?x1 - generic) - number
        (affinity ?x1 - generic ?x2 - generic) - number
    )

    (:action enabler_operator__find_errors
        :parameters (?x0 - generic)
        :precondition (and (not (has_done_find_errors ?x0 try_level_0)) (not (has_done_find_errors ?x0 try_level_1)))
        :effect (and
            (has_done_find_errors ?x0 try_level_0)
            (increase (total-cost) 5000))
    )

    (:action find_errors
        :parameters (?x0 - generic ?pre_level - num-retries ?post_level - num-retries)
        :precondition (and (mapped_to ?x0 database_link) (known database_link certain) (has_done_find_errors ?x0 ?pre_level) (not (has_done_find_errors ?x0 ?post_level)) (connected find_errors ?pre_level ?post_level))
        :effect (and
            (has_done find_errors present)
            (been_used ?x0)
            (been_used database_link)
            (has_done_find_errors ?x0 ?post_level)
            (free list_of_errors)
            (known list_of_errors certain)
            (not (mapped list_of_errors))
            (increase (total-cost) 10))
    )

    (:action enabler_operator__fix_errors
        :parameters (?x0 - generic)
        :precondition (and (not (has_done_fix_errors ?x0 try_level_0)) (not (has_done_fix_errors ?x0 try_level_1)))
        :effect (and
            (has_done_fix_errors ?x0 try_level_0)
            (increase (total-cost) 5000))
    )

    (:action fix_errors
        :parameters (?x0 - generic ?pre_level - num-retries ?post_level - num-retries)
        :precondition (and (mapped_to ?x0 list_of_errors) (known list_of_errors certain) (has_done_fix_errors ?x0 ?pre_level) (not (has_done_fix_errors ?x0 ?post_level)) (connected fix_errors ?pre_level ?post_level))
        :effect (and
            (has_done fix_errors present)
            (been_used ?x0)
            (been_used list_of_errors)
            (has_done_fix_errors ?x0 ?post_level)
            (increase (total-cost) 10))
    )

    (:action ask
        :parameters (?x - generic)
        :precondition (and (not (known ?x certain)) (not (not_slotfillable ?x)))
        :effect (and
            (free ?x)
            (mapped_to ?x ?x)
            (known ?x certain)
            (not (not_usable ?x))
            (not (mapped ?x))
            (increase (total-cost) (slot_goodness ?x)))
    )

    (:action map
        :parameters (?x - generic ?y - generic)
        :precondition (and (known ?x certain) (is_mappable ?x ?y) (not (not_mappable ?x ?y)) (not (mapped_to ?x ?y)) (not (new_item ?y)) (been_used ?y))
        :effect (and
            (known ?y certain)
            (mapped_to ?x ?y)
            (mapped ?x)
            (not (been_used ?y))
            (not (not_usable ?y))
            (increase (total-cost) (affinity ?x ?y)))
    )

    (:action map--free-alt
        :parameters (?x - generic ?y - generic)
        :precondition (and (known ?x certain) (is_mappable ?x ?y) (not (not_mappable ?x ?y)) (not (mapped_to ?x ?y)) (not (new_item ?y)) (been_used ?y) (free ?x))
        :effect (and
            (known ?y certain)
            (mapped_to ?x ?y)
            (mapped ?x)
            (not (been_used ?y))
            (not (not_usable ?y))
            (free ?y)
            (increase (total-cost) 1000))
    )

)