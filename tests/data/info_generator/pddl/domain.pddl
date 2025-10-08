(define (domain default_name-domain)
    (:requirements :typing :action-costs :equality)
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
        new_object_generic_0 v__0 v__1 v__2 v__3 v__4 v__5 v__6 - generic
        future past present - has-done-state
        try_level_0 try_level_1 try_level_2 try_level_3 try_level_4 try_level_5 try_level_6 - num-retries
        a__0 a__1 a__10 a__11 a__12 a__13 a__14 a__15 a__16 a__17 a__18 a__19 a__2 a__20 a__3 a__4 a__5 a__6 a__7 a__8 a__9 - operator
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
        (done_goal_pre )
        (done_goal_post )
        (has_done_a__13 ?x1 - generic ?x2 - generic ?x3 - num-retries)
        (has_done_a__7 ?x1 - generic ?x2 - generic ?x3 - num-retries)
        (has_done_a__12 ?x1 - generic ?x2 - generic ?x3 - num-retries)
        (has_done_a__19 ?x1 - generic ?x2 - generic ?x3 - num-retries)
        (has_done_a__2 ?x1 - generic ?x2 - generic ?x3 - num-retries)
        (has_done_a__16 ?x1 - generic ?x2 - generic ?x3 - num-retries)
        (has_done_a__18 ?x1 - generic ?x2 - generic ?x3 - num-retries)
        (has_done_a__17 ?x1 - generic ?x2 - generic ?x3 - num-retries)
        (has_done_a__1 ?x1 - generic ?x2 - generic ?x3 - num-retries)
        (has_done_a__4 ?x1 - generic ?x2 - generic ?x3 - num-retries)
        (has_done_a__20 ?x1 - generic ?x2 - generic ?x3 - num-retries)
        (has_done_a__3 ?x1 - generic ?x2 - generic ?x3 - num-retries)
        (has_done_a__5 ?x1 - generic ?x2 - generic ?x3 - num-retries)
        (has_done_a__11 ?x1 - generic ?x2 - generic ?x3 - num-retries)
        (has_done_a__8 ?x1 - generic ?x2 - generic ?x3 - num-retries)
        (has_done_a__9 ?x1 - generic ?x2 - generic ?x3 - num-retries)
        (has_done_a__15 ?x1 - generic ?x2 - generic ?x3 - num-retries)
        (has_done_a__10 ?x1 - generic ?x2 - generic ?x3 - num-retries)
        (has_done_a__14 ?x1 - generic ?x2 - generic ?x3 - num-retries)
        (has_done_a__6 ?x1 - generic ?x2 - generic ?x3 - num-retries)
        (has_done_a__0 ?x1 - generic ?x2 - generic ?x3 - num-retries)
    )

    (:functions
        (total-cost ) - number
        (slot_goodness ?x1 - generic) - number
        (affinity ?x1 - generic ?x2 - generic) - number
    )

    

    
    (:action enabler_operator__a__13
     :parameters (?x0 - generic ?x1 - generic)
     :precondition (and (not (has_done_a__13 ?x0 ?x1 try_level_0)) (not (has_done_a__13 ?x0 ?x1 try_level_1)))
     :effect (and
        (has_done_a__13 ?x0 ?x1 try_level_0)
        (increase (total-cost ) 5000))
    )


    (:action a__13
     :parameters (?x0 - generic ?x1 - generic ?pre_level - num-retries ?post_level - num-retries)
     :precondition (and (mapped_to ?x0 v__0) (known v__0 certain) (mapped_to ?x1 v__4) (known v__4 certain) (has_done_a__13 ?x0 ?x1 ?pre_level) (not (has_done_a__13 ?x0 ?x1 ?post_level)) (connected a__13 ?pre_level ?post_level))
     :effect (and
        (has_done a__13 present)
        (been_used ?x0)
        (been_used v__0)
        (been_used ?x1)
        (been_used v__4)
        (has_done_a__13 ?x0 ?x1 ?post_level)
        (free v__2)
        (known v__2 certain)
        (free v__1)
        (known v__1 certain)
        (not (mapped v__2))
        (not (mapped v__1))
        (increase (total-cost ) 10))
    )


    (:action enabler_operator__a__7
     :parameters (?x0 - generic ?x1 - generic)
     :precondition (and (not (has_done_a__7 ?x0 ?x1 try_level_0)) (not (has_done_a__7 ?x0 ?x1 try_level_1)))
     :effect (and
        (has_done_a__7 ?x0 ?x1 try_level_0)
        (increase (total-cost ) 5000))
    )


    (:action a__7
     :parameters (?x0 - generic ?x1 - generic ?pre_level - num-retries ?post_level - num-retries)
     :precondition (and (mapped_to ?x0 v__6) (known v__6 certain) (mapped_to ?x1 v__4) (known v__4 certain) (has_done_a__7 ?x0 ?x1 ?pre_level) (not (has_done_a__7 ?x0 ?x1 ?post_level)) (connected a__7 ?pre_level ?post_level))
     :effect (and
        (has_done a__7 present)
        (been_used ?x0)
        (been_used v__6)
        (been_used ?x1)
        (been_used v__4)
        (has_done_a__7 ?x0 ?x1 ?post_level)
        (free v__1)
        (known v__1 certain)
        (free v__2)
        (known v__2 certain)
        (not (mapped v__1))
        (not (mapped v__2))
        (increase (total-cost ) 10))
    )


    (:action enabler_operator__a__12
     :parameters (?x0 - generic ?x1 - generic)
     :precondition (and (not (has_done_a__12 ?x0 ?x1 try_level_0)) (not (has_done_a__12 ?x0 ?x1 try_level_1)))
     :effect (and
        (has_done_a__12 ?x0 ?x1 try_level_0)
        (increase (total-cost ) 5000))
    )


    (:action a__12
     :parameters (?x0 - generic ?x1 - generic ?pre_level - num-retries ?post_level - num-retries)
     :precondition (and (mapped_to ?x0 v__4) (known v__4 certain) (mapped_to ?x1 v__0) (known v__0 certain) (has_done_a__12 ?x0 ?x1 ?pre_level) (not (has_done_a__12 ?x0 ?x1 ?post_level)) (connected a__12 ?pre_level ?post_level))
     :effect (and
        (has_done a__12 present)
        (been_used ?x0)
        (been_used v__4)
        (been_used ?x1)
        (been_used v__0)
        (has_done_a__12 ?x0 ?x1 ?post_level)
        (free v__2)
        (known v__2 certain)
        (free v__1)
        (known v__1 certain)
        (not (mapped v__2))
        (not (mapped v__1))
        (increase (total-cost ) 10))
    )


    (:action enabler_operator__a__19
     :parameters (?x0 - generic ?x1 - generic)
     :precondition (and (not (has_done_a__19 ?x0 ?x1 try_level_0)) (not (has_done_a__19 ?x0 ?x1 try_level_1)))
     :effect (and
        (has_done_a__19 ?x0 ?x1 try_level_0)
        (increase (total-cost ) 5000))
    )


    (:action a__19
     :parameters (?x0 - generic ?x1 - generic ?pre_level - num-retries ?post_level - num-retries)
     :precondition (and (mapped_to ?x0 v__0) (known v__0 certain) (mapped_to ?x1 v__4) (known v__4 certain) (has_done_a__19 ?x0 ?x1 ?pre_level) (not (has_done_a__19 ?x0 ?x1 ?post_level)) (connected a__19 ?pre_level ?post_level))
     :effect (and
        (has_done a__19 present)
        (been_used ?x0)
        (been_used v__0)
        (been_used ?x1)
        (been_used v__4)
        (has_done_a__19 ?x0 ?x1 ?post_level)
        (free v__1)
        (known v__1 certain)
        (free v__2)
        (known v__2 certain)
        (not (mapped v__1))
        (not (mapped v__2))
        (increase (total-cost ) 10))
    )


    (:action enabler_operator__a__2
     :parameters (?x0 - generic ?x1 - generic)
     :precondition (and (not (has_done_a__2 ?x0 ?x1 try_level_0)) (not (has_done_a__2 ?x0 ?x1 try_level_1)))
     :effect (and
        (has_done_a__2 ?x0 ?x1 try_level_0)
        (increase (total-cost ) 5000))
    )


    (:action a__2
     :parameters (?x0 - generic ?x1 - generic ?pre_level - num-retries ?post_level - num-retries)
     :precondition (and (mapped_to ?x0 v__3) (known v__3 certain) (mapped_to ?x1 v__4) (known v__4 certain) (has_done_a__2 ?x0 ?x1 ?pre_level) (not (has_done_a__2 ?x0 ?x1 ?post_level)) (connected a__2 ?pre_level ?post_level))
     :effect (and
        (has_done a__2 present)
        (been_used ?x0)
        (been_used v__3)
        (been_used ?x1)
        (been_used v__4)
        (has_done_a__2 ?x0 ?x1 ?post_level)
        (free v__1)
        (known v__1 certain)
        (free v__6)
        (known v__6 certain)
        (not (mapped v__1))
        (not (mapped v__6))
        (increase (total-cost ) 10))
    )


    (:action enabler_operator__a__16
     :parameters (?x0 - generic ?x1 - generic)
     :precondition (and (not (has_done_a__16 ?x0 ?x1 try_level_0)) (not (has_done_a__16 ?x0 ?x1 try_level_1)))
     :effect (and
        (has_done_a__16 ?x0 ?x1 try_level_0)
        (increase (total-cost ) 5000))
    )


    (:action a__16
     :parameters (?x0 - generic ?x1 - generic ?pre_level - num-retries ?post_level - num-retries)
     :precondition (and (mapped_to ?x0 v__4) (known v__4 certain) (mapped_to ?x1 v__0) (known v__0 certain) (has_done_a__16 ?x0 ?x1 ?pre_level) (not (has_done_a__16 ?x0 ?x1 ?post_level)) (connected a__16 ?pre_level ?post_level))
     :effect (and
        (has_done a__16 present)
        (been_used ?x0)
        (been_used v__4)
        (been_used ?x1)
        (been_used v__0)
        (has_done_a__16 ?x0 ?x1 ?post_level)
        (free v__2)
        (known v__2 certain)
        (free v__1)
        (known v__1 certain)
        (not (mapped v__2))
        (not (mapped v__1))
        (increase (total-cost ) 10))
    )


    (:action enabler_operator__a__18
     :parameters (?x0 - generic ?x1 - generic)
     :precondition (and (not (has_done_a__18 ?x0 ?x1 try_level_0)) (not (has_done_a__18 ?x0 ?x1 try_level_1)))
     :effect (and
        (has_done_a__18 ?x0 ?x1 try_level_0)
        (increase (total-cost ) 5000))
    )


    (:action a__18
     :parameters (?x0 - generic ?x1 - generic ?pre_level - num-retries ?post_level - num-retries)
     :precondition (and (mapped_to ?x0 v__4) (known v__4 certain) (mapped_to ?x1 v__0) (known v__0 certain) (has_done_a__18 ?x0 ?x1 ?pre_level) (not (has_done_a__18 ?x0 ?x1 ?post_level)) (connected a__18 ?pre_level ?post_level))
     :effect (and
        (has_done a__18 present)
        (been_used ?x0)
        (been_used v__4)
        (been_used ?x1)
        (been_used v__0)
        (has_done_a__18 ?x0 ?x1 ?post_level)
        (free v__1)
        (known v__1 certain)
        (free v__2)
        (known v__2 certain)
        (not (mapped v__1))
        (not (mapped v__2))
        (increase (total-cost ) 10))
    )


    (:action enabler_operator__a__17
     :parameters (?x0 - generic ?x1 - generic)
     :precondition (and (not (has_done_a__17 ?x0 ?x1 try_level_0)) (not (has_done_a__17 ?x0 ?x1 try_level_1)))
     :effect (and
        (has_done_a__17 ?x0 ?x1 try_level_0)
        (increase (total-cost ) 5000))
    )


    (:action a__17
     :parameters (?x0 - generic ?x1 - generic ?pre_level - num-retries ?post_level - num-retries)
     :precondition (and (mapped_to ?x0 v__4) (known v__4 certain) (mapped_to ?x1 v__0) (known v__0 certain) (has_done_a__17 ?x0 ?x1 ?pre_level) (not (has_done_a__17 ?x0 ?x1 ?post_level)) (connected a__17 ?pre_level ?post_level))
     :effect (and
        (has_done a__17 present)
        (been_used ?x0)
        (been_used v__4)
        (been_used ?x1)
        (been_used v__0)
        (has_done_a__17 ?x0 ?x1 ?post_level)
        (free v__2)
        (known v__2 certain)
        (free v__1)
        (known v__1 certain)
        (not (mapped v__2))
        (not (mapped v__1))
        (increase (total-cost ) 10))
    )


    (:action enabler_operator__a__1
     :parameters (?x0 - generic ?x1 - generic)
     :precondition (and (not (has_done_a__1 ?x0 ?x1 try_level_0)) (not (has_done_a__1 ?x0 ?x1 try_level_1)))
     :effect (and
        (has_done_a__1 ?x0 ?x1 try_level_0)
        (increase (total-cost ) 5000))
    )


    (:action a__1
     :parameters (?x0 - generic ?x1 - generic ?pre_level - num-retries ?post_level - num-retries)
     :precondition (and (mapped_to ?x0 v__4) (known v__4 certain) (mapped_to ?x1 v__3) (known v__3 certain) (has_done_a__1 ?x0 ?x1 ?pre_level) (not (has_done_a__1 ?x0 ?x1 ?post_level)) (connected a__1 ?pre_level ?post_level))
     :effect (and
        (has_done a__1 present)
        (been_used ?x0)
        (been_used v__4)
        (been_used ?x1)
        (been_used v__3)
        (has_done_a__1 ?x0 ?x1 ?post_level)
        (free v__2)
        (known v__2 certain)
        (free v__5)
        (known v__5 certain)
        (not (mapped v__2))
        (not (mapped v__5))
        (increase (total-cost ) 10))
    )


    (:action enabler_operator__a__4
     :parameters (?x0 - generic ?x1 - generic)
     :precondition (and (not (has_done_a__4 ?x0 ?x1 try_level_0)) (not (has_done_a__4 ?x0 ?x1 try_level_1)))
     :effect (and
        (has_done_a__4 ?x0 ?x1 try_level_0)
        (increase (total-cost ) 5000))
    )


    (:action a__4
     :parameters (?x0 - generic ?x1 - generic ?pre_level - num-retries ?post_level - num-retries)
     :precondition (and (mapped_to ?x0 v__4) (known v__4 certain) (mapped_to ?x1 v__5) (known v__5 certain) (has_done_a__4 ?x0 ?x1 ?pre_level) (not (has_done_a__4 ?x0 ?x1 ?post_level)) (connected a__4 ?pre_level ?post_level))
     :effect (and
        (has_done a__4 present)
        (been_used ?x0)
        (been_used v__4)
        (been_used ?x1)
        (been_used v__5)
        (has_done_a__4 ?x0 ?x1 ?post_level)
        (free v__2)
        (known v__2 certain)
        (free v__6)
        (known v__6 certain)
        (not (mapped v__2))
        (not (mapped v__6))
        (increase (total-cost ) 10))
    )


    (:action enabler_operator__a__20
     :parameters (?x0 - generic ?x1 - generic)
     :precondition (and (not (has_done_a__20 ?x0 ?x1 try_level_0)) (not (has_done_a__20 ?x0 ?x1 try_level_1)))
     :effect (and
        (has_done_a__20 ?x0 ?x1 try_level_0)
        (increase (total-cost ) 5000))
    )


    (:action a__20
     :parameters (?x0 - generic ?x1 - generic ?pre_level - num-retries ?post_level - num-retries)
     :precondition (and (mapped_to ?x0 v__0) (known v__0 certain) (mapped_to ?x1 v__4) (known v__4 certain) (has_done_a__20 ?x0 ?x1 ?pre_level) (not (has_done_a__20 ?x0 ?x1 ?post_level)) (connected a__20 ?pre_level ?post_level))
     :effect (and
        (has_done a__20 present)
        (been_used ?x0)
        (been_used v__0)
        (been_used ?x1)
        (been_used v__4)
        (has_done_a__20 ?x0 ?x1 ?post_level)
        (free v__1)
        (known v__1 certain)
        (free v__2)
        (known v__2 certain)
        (not (mapped v__1))
        (not (mapped v__2))
        (increase (total-cost ) 10))
    )


    (:action enabler_operator__a__3
     :parameters (?x0 - generic ?x1 - generic)
     :precondition (and (not (has_done_a__3 ?x0 ?x1 try_level_0)) (not (has_done_a__3 ?x0 ?x1 try_level_1)))
     :effect (and
        (has_done_a__3 ?x0 ?x1 try_level_0)
        (increase (total-cost ) 5000))
    )


    (:action a__3
     :parameters (?x0 - generic ?x1 - generic ?pre_level - num-retries ?post_level - num-retries)
     :precondition (and (mapped_to ?x0 v__5) (known v__5 certain) (mapped_to ?x1 v__4) (known v__4 certain) (has_done_a__3 ?x0 ?x1 ?pre_level) (not (has_done_a__3 ?x0 ?x1 ?post_level)) (connected a__3 ?pre_level ?post_level))
     :effect (and
        (has_done a__3 present)
        (been_used ?x0)
        (been_used v__5)
        (been_used ?x1)
        (been_used v__4)
        (has_done_a__3 ?x0 ?x1 ?post_level)
        (free v__6)
        (known v__6 certain)
        (free v__1)
        (known v__1 certain)
        (not (mapped v__6))
        (not (mapped v__1))
        (increase (total-cost ) 10))
    )


    (:action enabler_operator__a__5
     :parameters (?x0 - generic ?x1 - generic)
     :precondition (and (not (has_done_a__5 ?x0 ?x1 try_level_0)) (not (has_done_a__5 ?x0 ?x1 try_level_1)))
     :effect (and
        (has_done_a__5 ?x0 ?x1 try_level_0)
        (increase (total-cost ) 5000))
    )


    (:action a__5
     :parameters (?x0 - generic ?x1 - generic ?pre_level - num-retries ?post_level - num-retries)
     :precondition (and (mapped_to ?x0 v__4) (known v__4 certain) (mapped_to ?x1 v__6) (known v__6 certain) (has_done_a__5 ?x0 ?x1 ?pre_level) (not (has_done_a__5 ?x0 ?x1 ?post_level)) (connected a__5 ?pre_level ?post_level))
     :effect (and
        (has_done a__5 present)
        (been_used ?x0)
        (been_used v__4)
        (been_used ?x1)
        (been_used v__6)
        (has_done_a__5 ?x0 ?x1 ?post_level)
        (free v__1)
        (known v__1 certain)
        (free v__2)
        (known v__2 certain)
        (not (mapped v__1))
        (not (mapped v__2))
        (increase (total-cost ) 10))
    )


    (:action enabler_operator__a__11
     :parameters (?x0 - generic ?x1 - generic)
     :precondition (and (not (has_done_a__11 ?x0 ?x1 try_level_0)) (not (has_done_a__11 ?x0 ?x1 try_level_1)))
     :effect (and
        (has_done_a__11 ?x0 ?x1 try_level_0)
        (increase (total-cost ) 5000))
    )


    (:action a__11
     :parameters (?x0 - generic ?x1 - generic ?pre_level - num-retries ?post_level - num-retries)
     :precondition (and (mapped_to ?x0 v__0) (known v__0 certain) (mapped_to ?x1 v__4) (known v__4 certain) (has_done_a__11 ?x0 ?x1 ?pre_level) (not (has_done_a__11 ?x0 ?x1 ?post_level)) (connected a__11 ?pre_level ?post_level))
     :effect (and
        (has_done a__11 present)
        (been_used ?x0)
        (been_used v__0)
        (been_used ?x1)
        (been_used v__4)
        (has_done_a__11 ?x0 ?x1 ?post_level)
        (free v__1)
        (known v__1 certain)
        (free v__2)
        (known v__2 certain)
        (not (mapped v__1))
        (not (mapped v__2))
        (increase (total-cost ) 10))
    )


    (:action enabler_operator__a__8
     :parameters (?x0 - generic ?x1 - generic)
     :precondition (and (not (has_done_a__8 ?x0 ?x1 try_level_0)) (not (has_done_a__8 ?x0 ?x1 try_level_1)))
     :effect (and
        (has_done_a__8 ?x0 ?x1 try_level_0)
        (increase (total-cost ) 5000))
    )


    (:action a__8
     :parameters (?x0 - generic ?x1 - generic ?pre_level - num-retries ?post_level - num-retries)
     :precondition (and (mapped_to ?x0 v__6) (known v__6 certain) (mapped_to ?x1 v__4) (known v__4 certain) (has_done_a__8 ?x0 ?x1 ?pre_level) (not (has_done_a__8 ?x0 ?x1 ?post_level)) (connected a__8 ?pre_level ?post_level))
     :effect (and
        (has_done a__8 present)
        (been_used ?x0)
        (been_used v__6)
        (been_used ?x1)
        (been_used v__4)
        (has_done_a__8 ?x0 ?x1 ?post_level)
        (free v__1)
        (known v__1 certain)
        (free v__2)
        (known v__2 certain)
        (not (mapped v__1))
        (not (mapped v__2))
        (increase (total-cost ) 10))
    )


    (:action enabler_operator__a__9
     :parameters (?x0 - generic ?x1 - generic)
     :precondition (and (not (has_done_a__9 ?x0 ?x1 try_level_0)) (not (has_done_a__9 ?x0 ?x1 try_level_1)))
     :effect (and
        (has_done_a__9 ?x0 ?x1 try_level_0)
        (increase (total-cost ) 5000))
    )


    (:action a__9
     :parameters (?x0 - generic ?x1 - generic ?pre_level - num-retries ?post_level - num-retries)
     :precondition (and (mapped_to ?x0 v__6) (known v__6 certain) (mapped_to ?x1 v__4) (known v__4 certain) (has_done_a__9 ?x0 ?x1 ?pre_level) (not (has_done_a__9 ?x0 ?x1 ?post_level)) (connected a__9 ?pre_level ?post_level))
     :effect (and
        (has_done a__9 present)
        (been_used ?x0)
        (been_used v__6)
        (been_used ?x1)
        (been_used v__4)
        (has_done_a__9 ?x0 ?x1 ?post_level)
        (free v__1)
        (known v__1 certain)
        (free v__2)
        (known v__2 certain)
        (not (mapped v__1))
        (not (mapped v__2))
        (increase (total-cost ) 10))
    )


    (:action enabler_operator__a__15
     :parameters (?x0 - generic ?x1 - generic)
     :precondition (and (not (has_done_a__15 ?x0 ?x1 try_level_0)) (not (has_done_a__15 ?x0 ?x1 try_level_1)))
     :effect (and
        (has_done_a__15 ?x0 ?x1 try_level_0)
        (increase (total-cost ) 5000))
    )


    (:action a__15
     :parameters (?x0 - generic ?x1 - generic ?pre_level - num-retries ?post_level - num-retries)
     :precondition (and (mapped_to ?x0 v__4) (known v__4 certain) (mapped_to ?x1 v__0) (known v__0 certain) (has_done_a__15 ?x0 ?x1 ?pre_level) (not (has_done_a__15 ?x0 ?x1 ?post_level)) (connected a__15 ?pre_level ?post_level))
     :effect (and
        (has_done a__15 present)
        (been_used ?x0)
        (been_used v__4)
        (been_used ?x1)
        (been_used v__0)
        (has_done_a__15 ?x0 ?x1 ?post_level)
        (free v__1)
        (known v__1 certain)
        (free v__2)
        (known v__2 certain)
        (not (mapped v__1))
        (not (mapped v__2))
        (increase (total-cost ) 10))
    )


    (:action enabler_operator__a__10
     :parameters (?x0 - generic ?x1 - generic)
     :precondition (and (not (has_done_a__10 ?x0 ?x1 try_level_0)) (not (has_done_a__10 ?x0 ?x1 try_level_1)))
     :effect (and
        (has_done_a__10 ?x0 ?x1 try_level_0)
        (increase (total-cost ) 5000))
    )


    (:action a__10
     :parameters (?x0 - generic ?x1 - generic ?pre_level - num-retries ?post_level - num-retries)
     :precondition (and (mapped_to ?x0 v__4) (known v__4 certain) (mapped_to ?x1 v__6) (known v__6 certain) (has_done_a__10 ?x0 ?x1 ?pre_level) (not (has_done_a__10 ?x0 ?x1 ?post_level)) (connected a__10 ?pre_level ?post_level))
     :effect (and
        (has_done a__10 present)
        (been_used ?x0)
        (been_used v__4)
        (been_used ?x1)
        (been_used v__6)
        (has_done_a__10 ?x0 ?x1 ?post_level)
        (free v__2)
        (known v__2 certain)
        (free v__1)
        (known v__1 certain)
        (not (mapped v__2))
        (not (mapped v__1))
        (increase (total-cost ) 10))
    )


    (:action enabler_operator__a__14
     :parameters (?x0 - generic ?x1 - generic)
     :precondition (and (not (has_done_a__14 ?x0 ?x1 try_level_0)) (not (has_done_a__14 ?x0 ?x1 try_level_1)))
     :effect (and
        (has_done_a__14 ?x0 ?x1 try_level_0)
        (increase (total-cost ) 5000))
    )


    (:action a__14
     :parameters (?x0 - generic ?x1 - generic ?pre_level - num-retries ?post_level - num-retries)
     :precondition (and (mapped_to ?x0 v__4) (known v__4 certain) (mapped_to ?x1 v__0) (known v__0 certain) (has_done_a__14 ?x0 ?x1 ?pre_level) (not (has_done_a__14 ?x0 ?x1 ?post_level)) (connected a__14 ?pre_level ?post_level))
     :effect (and
        (has_done a__14 present)
        (been_used ?x0)
        (been_used v__4)
        (been_used ?x1)
        (been_used v__0)
        (has_done_a__14 ?x0 ?x1 ?post_level)
        (free v__2)
        (known v__2 certain)
        (free v__1)
        (known v__1 certain)
        (not (mapped v__2))
        (not (mapped v__1))
        (increase (total-cost ) 10))
    )


    (:action enabler_operator__a__6
     :parameters (?x0 - generic ?x1 - generic)
     :precondition (and (not (has_done_a__6 ?x0 ?x1 try_level_0)) (not (has_done_a__6 ?x0 ?x1 try_level_1)))
     :effect (and
        (has_done_a__6 ?x0 ?x1 try_level_0)
        (increase (total-cost ) 5000))
    )


    (:action a__6
     :parameters (?x0 - generic ?x1 - generic ?pre_level - num-retries ?post_level - num-retries)
     :precondition (and (mapped_to ?x0 v__4) (known v__4 certain) (mapped_to ?x1 v__6) (known v__6 certain) (has_done_a__6 ?x0 ?x1 ?pre_level) (not (has_done_a__6 ?x0 ?x1 ?post_level)) (connected a__6 ?pre_level ?post_level))
     :effect (and
        (has_done a__6 present)
        (been_used ?x0)
        (been_used v__4)
        (been_used ?x1)
        (been_used v__6)
        (has_done_a__6 ?x0 ?x1 ?post_level)
        (free v__2)
        (known v__2 certain)
        (free v__6)
        (known v__6 certain)
        (not (mapped v__2))
        (not (mapped v__6))
        (increase (total-cost ) 10))
    )


    (:action enabler_operator__a__0
     :parameters (?x0 - generic ?x1 - generic)
     :precondition (and (not (has_done_a__0 ?x0 ?x1 try_level_0)) (not (has_done_a__0 ?x0 ?x1 try_level_1)))
     :effect (and
        (has_done_a__0 ?x0 ?x1 try_level_0)
        (increase (total-cost ) 5000))
    )


    (:action a__0
     :parameters (?x0 - generic ?x1 - generic ?pre_level - num-retries ?post_level - num-retries)
     :precondition (and (mapped_to ?x0 v__4) (known v__4 certain) (mapped_to ?x1 v__0) (known v__0 certain) (has_done_a__0 ?x0 ?x1 ?pre_level) (not (has_done_a__0 ?x0 ?x1 ?post_level)) (connected a__0 ?pre_level ?post_level))
     :effect (and
        (has_done a__0 present)
        (been_used ?x0)
        (been_used v__4)
        (been_used ?x1)
        (been_used v__0)
        (has_done_a__0 ?x0 ?x1 ?post_level)
        (free v__3)
        (known v__3 certain)
        (free v__1)
        (known v__1 certain)
        (not (mapped v__3))
        (not (mapped v__1))
        (increase (total-cost ) 10))
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
        (increase (total-cost ) (slot_goodness ?x)))
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
        (increase (total-cost ) (affinity ?x ?y)))
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
        (increase (total-cost ) 1000))
    )

)