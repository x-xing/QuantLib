
#%%
from QuantLib import *

class ShortRateModelTest:
    def testSwaps(self):
        print("Testing Hull-White swap pricing against known values...")
        
        calendar = TARGET()
        today = Date.todaysDate()
        Settings.instance().evaluationDate = calendar.adjust(today)
        settlement = calendar.advance(today, 2, Days)


        dates = [settlement,
                calendar.advance(settlement,1,Weeks),
                calendar.advance(settlement,1,Months),
                calendar.advance(settlement,3,Months),
                calendar.advance(settlement,6,Months),
                calendar.advance(settlement,9,Months),
                calendar.advance(settlement,1,Years),
                calendar.advance(settlement,2,Years),
                calendar.advance(settlement,3,Years),
                calendar.advance(settlement,5,Years),
                calendar.advance(settlement,10,Years),
                calendar.advance(settlement,15,Years)]
        
        discountFactors = [ 1.0, 0.999258, 0.996704, 0.990809, 0.981798, 
                            0.972570, 0.963430, 0.929532, 0.889267,
                            0.803693, 0.596903, 0.433022]
    
        termStructure = YieldTermStructureHandle(DiscountCurve( dates, 
                                                                discountFactors,
                                                                Actual365Fixed()))
        model = HullWhite(termStructure)

        start = [ -3, 0, 3 ]
        length = [ 2, 5, 10 ]
        rates = [ 0.02, 0.04, 0.06 ]
        euribor = Euribor6M(termStructure)
        engine = TreeSwaptionEngine(model, 120)

        tolerance = 1e-8

        for s in start:
            startDate = calendar.advance(settlement,s,Months)
            if startDate < today:
                fixingDate = calendar.advance(startDate,-2,Days)
            pastFixings = RealTimeSeries([fixingDate], [0.03])
            IndexManager.instance().setHistory(euribor.name(),
                                               pastFixings)
        
        for l in length:
            maturity = calendar.advance(startDate,l,Years)
            fixedSchedule = Schedule(startDate, maturity, Period(Annual),
                                     calendar, Unadjusted, Unadjusted,
                                     DateGeneration.Forward, False)
            floatSchedule = Schedule(startDate, maturity, Period(Semiannual),
                                     calendar, Following, Following,
                                     DateGeneration.Forward, False)
            for r in rates:
                swap = VanillaSwap(VanillaSwap.Payer, 1000000.0,
                                   fixedSchedule, r, Thirty360(),
                                   floatSchedule, euribor, 0.0, Actual360())

                swap.setPricingEngine(DiscountingSwapEngine(termStructure))
                expected = swap.NPV()
                #swap.setPricingEngine(engine)
                #calculated = swap.NPV()

                #error = (expected-calculated)/expected
                print(expected)
                
srt = ShortRateModelTest()
srt.testSwaps()

#%%
help(PricingEngine)

#%%

    

    for (Size i=0; i<LENGTH(start); i++) {

        Date startDate = calendar.advance(settlement,start[i],Months);
        if (startDate < today) {
            Date fixingDate = calendar.advance(startDate,-2,Days);
            TimeSeries<Real> pastFixings;
            pastFixings[fixingDate] = 0.03;
            IndexManager::instance().setHistory(euribor->name(),
                                                pastFixings);
        }

        for (Size j=0; j<LENGTH(length); j++) {

            Date maturity = calendar.advance(startDate,length[i],Years);
            Schedule fixedSchedule(startDate, maturity, Period(Annual),
                                   calendar, Unadjusted, Unadjusted,
                                   DateGeneration::Forward, false);
            Schedule floatSchedule(startDate, maturity, Period(Semiannual),
                                   calendar, Following, Following,
                                   DateGeneration::Forward, false);
            for (Size k=0; k<LENGTH(rates); k++) {

                VanillaSwap swap(VanillaSwap::Payer, 1000000.0,
                                 fixedSchedule, rates[k], Thirty360(),
                                 floatSchedule, euribor, 0.0, Actual360());
                swap.setPricingEngine(ext::shared_ptr<PricingEngine>(
                                   new DiscountingSwapEngine(termStructure)));
                Real expected = swap.NPV();
                swap.setPricingEngine(engine);
                Real calculated = swap.NPV();

                Real error = std::fabs((expected-calculated)/expected);
                if (error > tolerance) {
                    BOOST_ERROR("Failed to reproduce swap NPV:"
                                << std::fixed << std::setprecision(9)
                                << "\n    calculated: " << calculated
                                << "\n    expected:   " << expected
                                << std::scientific
                                << "\n    rel. error: " << error);
                }
            }
        }
    }
    '''
    static void testFuturesConvexityBias()
    static void testCachedHullWhite();
    static void testCachedHullWhiteFixedReversion();
    static void testCachedHullWhite2();
    static void testSwaps();
    static void testExtendedCoxIngersollRossDiscountFactor();
    static boost::unit_test_framework::test_suite* suite(SpeedLevel);
    '''


class Employee:
   'Common base class for all employees'
   empCount = 0

   def __init__(self, name, salary):
      self.name = name
      self.salary = salary
      Employee.empCount += 1
   
   def displayCount(self):
     print "Total Employee %d" % Employee.empCount

   def displayEmployee(self):
      print "Name : ", self.name,  ", Salary: ", self.salary


#%%
