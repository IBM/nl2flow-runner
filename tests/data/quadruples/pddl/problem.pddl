(define (problem basic_test-problem)
    (:domain basic_test-domain)

    (:objects

    )

    (:init
        (= (slot_goodness database_link) 150000.0)
        (= (slot_goodness list_of_errors) 150000.0)
        (= (slot_goodness new_object_generic_0) 150000.0)
        (= (total-cost) 0.0)
        (been_used database_link)
        (been_used list_of_errors)
        (connected fix_errors try_level_0 try_level_1)
        (connected find_errors try_level_0 try_level_1)
        (new_item new_object_generic_0)
        (mapped_to new_object_generic_0 new_object_generic_0)
        (mapped_to list_of_errors list_of_errors)
        (mapped_to database_link database_link)
    )

    (:goal
        (has_done fix_errors present)
    )

    (:metric minimize
        (total-cost)
    )
)