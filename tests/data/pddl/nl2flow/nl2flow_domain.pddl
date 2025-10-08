(define (domain default_name-domain)
    (:requirements :equality :action-costs :typing :negative-preconditions :fluents)
    (:types
        generic - object
        operator - object
        has-done-state - object
        constraint-status - object
        datum-state - object
        label - object
        object
    )

    (:constants
        False True - constraint-status
        certain uncertain unknown - datum-state
        new_object_generic_0 v__0 v__1 v__10 v__11 v__12 v__13 v__14 v__15 v__16 v__17 v__18 v__19 v__2 v__20 v__21 v__22 v__23 v__24 v__25 v__26 v__27 v__28 v__29 v__3 v__4 v__5 v__6 v__7 v__8 v__9 - generic
        future past present - has-done-state
        a__0 a__1 a__2 - operator
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
        (free ?x1 - generic)
        (done_goal_pre)
        (done_goal_post)
    )

    (:functions
        (total-cost) - number
        (slot_goodness ?x1 - generic) - number
        (affinity ?x1 - generic ?x2 - generic) - number
    )

    (:action a__1
        :parameters ()
        :precondition (and (not (has_done a__1 past)) (and (known v__11 certain) (and (known v__12 certain) (known v__13 certain))))
        :effect (and
            (has_done a__1 present)
            (been_used v__11)
            (been_used v__12)
            (been_used v__13)
            (free v__15)
            (known v__15 certain)
            (free v__18)
            (known v__18 certain)
            (free v__16)
            (known v__16 certain)
            (not (mapped v__15))
            (not (mapped v__18))
            (not (mapped v__16))
            (increase (total-cost) 10))
    )

    (:action a__2
        :parameters ()
        :precondition (and (not (has_done a__2 past)) (and (known v__20 certain) (and (known v__23 certain) (known v__21 certain))))
        :effect (and
            (has_done a__2 present)
            (been_used v__20)
            (been_used v__23)
            (been_used v__21)
            (free v__26)
            (known v__26 certain)
            (free v__28)
            (known v__28 certain)
            (free v__27)
            (known v__27 certain)
            (not (mapped v__26))
            (not (mapped v__28))
            (not (mapped v__27))
            (increase (total-cost) 10))
    )

    (:action a__0
        :parameters ()
        :precondition (and (not (has_done a__0 past)) (and (known v__3 certain) (and (known v__0 certain) (known v__2 certain))))
        :effect (and
            (has_done a__0 present)
            (been_used v__3)
            (been_used v__0)
            (been_used v__2)
            (free v__5)
            (known v__5 certain)
            (free v__4)
            (known v__4 certain)
            (free v__6)
            (known v__6 certain)
            (not (mapped v__5))
            (not (mapped v__4))
            (not (mapped v__6))
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

)