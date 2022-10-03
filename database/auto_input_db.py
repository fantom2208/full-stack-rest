# module to insert initial data to all tables 

# import os module to check current folder
import os


# from initial setup module import CLASSES 
db_fldr_flag = os.getcwd().split('/')[-1] == 'database'
if db_fldr_flag:
    from database_setup import Base, MenuItem, Restaurant, \
                               RestMenuItem, get_db_connection
else:
    from database.database_setup import Base, MenuItem, Restaurant, \
                                        RestMenuItem, get_db_connection



def show_restaurants(rest_ses):
    # check - session query to all Restaurant records
    qr_res = rest_ses.query(Restaurant).all()
    result='Total list of restaurants:\n'
    for item in qr_res:
        result = result + '{} - {}\n'.format(item.id, item.name)
    return result


def show_menu_items(rest_ses):
    # check - session query to all Restaurant records
    qr_res = rest_ses.query(MenuItem).all()
    result='Total list of menu items:\n'
    for item in qr_res:
        result = result + '{} - {} - {}\n'.format(item.id, item.name, item.description)
    return result


def show_rest_menu_items(rest_ses):
    # check - session query to all Restaurant records
    qr_res = rest_ses.query(RestMenuItem).all()
    result='Total list of menu items prices:\n'
    for item in qr_res:
        result = result + '{} - {} - {} - {}\n'.format(item.id, item.restaurant_id, item.menu_item_id, item.price)
    return result 
    

def init_all_tables(rest_ses):
    # add restaurants
    TopBurger = Restaurant(name = 'Top Burger', 
                           description = 'Home restaurant at the historical center of the town',
                           address = 'Hloria, Middle street, 12')
    rest_ses.add(TopBurger)

    TacoHut = Restaurant(name = 'Taco Hut', 
                         description = 'Mexican restaurant at the town',
                         address = 'Raho, Central street, 32')
    rest_ses.add(TacoHut)

    SuperStirFry = Restaurant(name = 'Super Stir Fry',
                                description = 'Restaurant of all fry food at the town',
                                address = 'Townsquare, Side street, 2')
    rest_ses.add(SuperStirFry)

    BlueBurgers = Restaurant(name = 'Blue Burgers', 
                             description = 'Nice restaurant at the town',
                             address = 'Georgia, Central square, 2')
    rest_ses.add(BlueBurgers)

    PandaGarden = Restaurant(name = "Panda Garden",
                             description = 'Nice China restaurant with homemade dishes',
                             address = 'Kaltaki, Central street, 12')
    rest_ses.add(PandaGarden)

    UrbanBurger = Restaurant(name = "Urban Burger",
                             description = 'Modern restaurant at trade center of the town',
                             address = 'Palaster, Trade street, 142a')
    rest_ses.add(UrbanBurger)

    # commit changes
    rest_ses.commit()
    if db_fldr_flag:
        # check - session query to all Restaurant records
        print(show_restaurants(rest_ses))


    # add menu items
    PizzaCheese = MenuItem(name = 'Pizza cheese', 
                           description = 'Nice pizza with Mozzarella and Lamber, D = 42 cm',
                           course = 'Entree',
                           weight = 800,
                           content = 'Flour, water, salt, tomato souce, Mozzarella and Lamber cheeses')
    rest_ses.add(PizzaCheese)



    FrenchFries = MenuItem(name = "French Fries", 
                           description = "with garlic and parmesan", 
                           course = "Entree", 
                           weight = 200,
                           content = 'Potatos, sunflower oil')
    rest_ses.add(FrenchFries)
    ChickenStirFry = MenuItem(name = "Chicken Stir Fry", 
                              description = "With your choice of noodles vegetables and sauces", 
                              course = "Entree", 
                              weight = 400)
    rest_ses.add(ChickenStirFry)  



    MushroomRisotto = MenuItem(name = "Mushroom risotto", 
                               description = "Portabello mushrooms in a creamy risotto", 
                               course = "Entree", 
                               weight = 300)
    rest_ses.add(MushroomRisotto)
    PekingDuck  = MenuItem(name = "Peking Duck", 
                           description = " A famous duck dish from Beijing[1] that has been prepared since the imperial era. The meat is prized for its thin, crisp skin, with authentic versions of the dish serving mostly the skin and little meat, sliced in front of the diners by the cook", 
                           course = "Entree", 
                           weight = 450)
    rest_ses.add(PekingDuck)
    NepaliMomo  = MenuItem(name = "Nepali Momo", 
                           description = "Steamed dumplings made with vegetables, spices and meat. ", 
                           course = "Entree", 
                           weight = 450)
    rest_ses.add(NepaliMomo)
    ChineseDumplings = MenuItem(name = "Chinese Dumplings", 
                                description = "a common Chinese dumpling which generally consists of minced meat and finely chopped vegetables wrapped into a piece of dough skin. The skin can be either thin and elastic or thicker.", 
                                course = "Entree", 
                                weight = 400)
    rest_ses.add(ChineseDumplings)
    ChickenAndRice = MenuItem(name = "Chicken and Rice", 
                              description = "Chicken... and rice",
                              course = "Entree", 
                              weight = 300)
    rest_ses.add(ChickenAndRice)
    MomsSpaghetti = MenuItem(name = "Mom's Spaghetti", 
                             description = "Spaghetti with some incredible tomato sauce made by mom", 
                             course = "Entree", 
                             weight = 300)
    rest_ses.add(MomsSpaghetti)                    





    VeggieBurger = MenuItem(name = "Veggie Burger", 
                            description = "Juicy grilled veggie patty with tomato mayo and lettuce", 
                            course = "Entree",
                            weight = 400)
    rest_ses.add(VeggieBurger)
    ChickenBurger = MenuItem(name = "Chicken Burger", 
                            description = "Juicy grilled chicken patty with tomato mayo and lettuce", 
                            course = "Entree",
                            weight = 350)
    rest_ses.add(ChickenBurger)
    SirloinBurger = MenuItem(name = "Sirloin Burger", 
                             description = "Made with grade A beef", 
                             course = "Entree", 
                             weight = 300)
    rest_ses.add(SirloinBurger)
    GrilledCheeseSandwich = MenuItem(name = "Grilled Cheese Sandwich", 
                                     description = "On texas toast with American Cheese",
                                     course = "Entree", 
                                     weight = 300)
    rest_ses.add(GrilledCheeseSandwich)


    BeefNoodleSoup = MenuItem(name = "Beef Noodle Soup", 
                              description = "A Chinese noodle soup made of stewed or red braised beef, beef broth, vegetables and Chinese noodles.", 
                              course = "Entree", 
                              weight = 300)
    rest_ses.add(BeefNoodleSoup)
    Ramen = MenuItem(name = "Ramen", 
                     description = "a Japanese noodle soup dish. It consists of Chinese-style wheat noodles served in a meat- or (occasionally) fish-based broth, often flavored with soy sauce or miso, and uses toppings such as sliced pork, dried seaweed, kamaboko, and green onions.", 
                     course = "Entree", 
                     weight = 250)
    rest_ses.add(Ramen)
    Pho = MenuItem(name = "Pho", 
                   description = "a Vietnamese noodle soup consisting of broth, linguine-shaped rice noodles called banh pho, a few herbs, and meat.", 
                   course = "Entree", 
                   weight = 250)
    rest_ses.add(Pho)


    ChocolateCake = MenuItem(name = 'Chocolate Cake',
                            description = 'made with Dutch Chocolate',
                            course = 'Dessert',
                            weight = 100,
                            content = '')
    rest_ses.add(ChocolateCake)
    TresLechesCake = MenuItem(name = "Tres Leches Cake", 
                              description = "Rich, luscious sponge cake soaked in sweet milk and topped with vanilla bean whipped cream and strawberries.", 
                              course = "Dessert", 
                              weight = 100)
    rest_ses.add(TresLechesCake)
    HoneyBobaShavedSnow = MenuItem(name = "Honey Boba Shaved Snow", 
                                   description = "Milk snow layered with honey boba, jasmine tea jelly, grass jelly, caramel, cream, and freshly made mochi", 
                                   course = "Dessert", 
                                   weight = 170)
    rest_ses.add(HoneyBobaShavedSnow)
    BoysenberrySorbet = MenuItem(name = "Boysenberry Sorbet", 
                                 description = "An unsettlingly huge amount of ripe berries turned into frozen (and seedless) awesomeness", 
                                 course = "Dessert", 
                                 weight = 140)
    rest_ses.add(BoysenberrySorbet)



    RootBeer = MenuItem(name = "Root Beer", 
                        description = "super refreshing goodness",  
                        course = "Beverage", 
                        weight = 500)
    rest_ses.add(RootBeer)
    WheatBeer = MenuItem(name = "Wheat Beer", 
                        description = "craft non filtered beer",  
                        course = "Beverage", 
                        weight = 450)
    rest_ses.add(WheatBeer)
    Lager = MenuItem(name = "Lager", 
                        description = "craft lager beer",  
                        course = "Beverage", 
                        weight = 500)
    rest_ses.add(Lager)


    IcedTea = MenuItem(name = "Iced Tea", 
                       description = "with Lemon", 
                       course = "Beverage", 
                       weight = 400)
    rest_ses.add(IcedTea)
    BlackTea = MenuItem(name = "Classic black tea", 
                       description = "very strong taste", 
                       course = "Beverage", 
                       weight = 200)
    rest_ses.add(BlackTea)
    Americano = MenuItem(name = "Americano", 
                       description = "very strong taste", 
                       course = "Beverage", 
                       weight = 300)
    rest_ses.add(Americano)



    Gyoza = MenuItem(name = "Gyoza", 
                     description = "The most prominent differences between Japanese-style gyoza and Chinese-style jiaozi are the rich garlic flavor, which is less noticeable in the Chinese version, the light seasoning of Japanese gyoza with salt and soy sauce, and the fact that gyoza wrappers are much thinner", 
                     course = "Entree", 
                     weight = 300)
    rest_ses.add(Gyoza)
    StinkyTofu = MenuItem(name = "Stinky Tofu", 
                              description = "Taiwanese dish, deep fried fermented tofu served with pickled cabbage.", 
                              course = "Entree", 
                              weight = 200)
    rest_ses.add(StinkyTofu)
    SpicyTunaRoll = MenuItem(name = "Spicy Tuna Roll", 
                             description = "Seared rare ahi, avocado, edamame, cucumber with wasabi soy sauce ", 
                             course = "Entree",
                             weight = 150)
    rest_ses.add(SpicyTunaRoll)

    

    # commit changes
    rest_ses.commit()
    if db_fldr_flag:
        # check - session query to all MenuItem records
        print(show_menu_items(rest_ses))


    # add menu with prices for restaurants
    #Menu for UrbanBurger
    menuItem = RestMenuItem(restaurant = UrbanBurger, 
                            menu_item = VeggieBurger, 
                            price = 350,
                            comment = "New taste for this summer!")
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = UrbanBurger, 
                            menu_item = FrenchFries, 
                            price = 200)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = UrbanBurger, 
                            menu_item = ChickenBurger, 
                            price = 450)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = UrbanBurger, 
                            menu_item = SirloinBurger, 
                            price = 550)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = UrbanBurger, 
                            menu_item = RootBeer, 
                            price = 350)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = UrbanBurger, 
                            menu_item = Lager, 
                            price = 250)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = UrbanBurger, 
                            menu_item = GrilledCheeseSandwich, 
                            price = 370)
    rest_ses.add(menuItem)
    rest_ses.commit()


    #Menu for Super Stir Fry
    menuItem = RestMenuItem(restaurant = SuperStirFry, 
                            menu_item = ChickenStirFry, 
                            price = 350,
                            comment = "Promo price")
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = SuperStirFry, 
                            menu_item = PekingDuck, 
                            price = 550)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = SuperStirFry, 
                            menu_item = NepaliMomo, 
                            price = 650,
                            comment = "New taste")
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = SuperStirFry, 
                            menu_item = BeefNoodleSoup, 
                            price = 450)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = SuperStirFry, 
                            menu_item = Ramen, 
                            price = 450)
    rest_ses.add(menuItem)
    rest_ses.commit()


    #Menu for Panda Garden
    menuItem = RestMenuItem(restaurant = PandaGarden, 
                            menu_item = Ramen, 
                            price = 400)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = PandaGarden, 
                            menu_item = Pho, 
                            price = 530)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = PandaGarden, 
                            menu_item = ChineseDumplings, 
                            price = 430)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = PandaGarden, 
                            menu_item = Gyoza, 
                            price = 380)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = PandaGarden, 
                            menu_item = StinkyTofu, 
                            price = 580,
                            comment = 'Very nice taste')
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = PandaGarden, 
                            menu_item = SpicyTunaRoll, 
                            price = 340,
                            comment = 'New')
    rest_ses.add(menuItem)
    rest_ses.commit()

        #Menu for Taco Hut
    menuItem = RestMenuItem(restaurant = TacoHut, 
                            menu_item = FrenchFries, 
                            price = 210)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = TacoHut, 
                            menu_item = ChickenStirFry, 
                            price = 330)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = TacoHut, 
                            menu_item = MushroomRisotto, 
                            price = 430)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = TacoHut, 
                            menu_item = NepaliMomo, 
                            price = 380)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = TacoHut, 
                            menu_item = ChickenAndRice, 
                            price = 580,
                            comment = 'New taste')
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = TacoHut, 
                            menu_item = GrilledCheeseSandwich, 
                            price = 340,
                            comment = 'promo price')
    rest_ses.add(menuItem)
    rest_ses.commit()

    #Menu for Top Burger
    menuItem = RestMenuItem(restaurant = TopBurger, 
                            menu_item = VeggieBurger, 
                            price = 330,
                            comment = "lower price")
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = TopBurger, 
                            menu_item = FrenchFries, 
                            price = 190)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = TopBurger, 
                            menu_item = ChickenBurger, 
                            price = 480)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = TopBurger, 
                            menu_item = PizzaCheese, 
                            price = 580,
                            comment =  'pizza taste')
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = TopBurger, 
                            menu_item = RootBeer, 
                            price = 400)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = TopBurger, 
                            menu_item = Lager, 
                            price = 300)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = TopBurger, 
                            menu_item = GrilledCheeseSandwich, 
                            price = 370)
    rest_ses.add(menuItem)

    menuItem = RestMenuItem(restaurant = TopBurger, 
                            menu_item = ChocolateCake, 
                            price = 270,
                            comment = 'our sweets')
    menuItem = RestMenuItem(restaurant = TopBurger, 
                            menu_item = TresLechesCake, 
                            price = 280,
                            comment = 'our sweets')
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = TopBurger, 
                            menu_item = IcedTea, 
                            price = 180)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = TopBurger, 
                            menu_item = BlackTea, 
                            price = 180)
    rest_ses.add(menuItem)
    rest_ses.commit()

     #Menu for BlueBurgers
    menuItem = RestMenuItem(restaurant = BlueBurgers, 
                            menu_item = VeggieBurger, 
                            price = 430)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = BlueBurgers, 
                            menu_item = FrenchFries, 
                            price = 190)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = BlueBurgers, 
                            menu_item = ChickenBurger, 
                            price = 480)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = BlueBurgers, 
                            menu_item = ChickenAndRice, 
                            price = 580)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = BlueBurgers, 
                            menu_item = RootBeer, 
                            price = 400)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = BlueBurgers, 
                            menu_item = Lager, 
                            price = 300)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = BlueBurgers, 
                            menu_item = GrilledCheeseSandwich, 
                            price = 370)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = BlueBurgers, 
                            menu_item = WheatBeer, 
                            price = 270)
    menuItem = RestMenuItem(restaurant = BlueBurgers, 
                            menu_item = BeefNoodleSoup, 
                            price = 280,
                            comment = 'new and promo')
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = BlueBurgers, 
                            menu_item = Americano, 
                            price = 230)
    rest_ses.add(menuItem)
    menuItem = RestMenuItem(restaurant = BlueBurgers, 
                            menu_item = BlackTea, 
                            price = 180)
    rest_ses.add(menuItem)
    rest_ses.commit()



    if db_fldr_flag:
        # print list of restaurants menus
        print(show_rest_menu_items(rest_ses))


    return 'Initialiazation was Ok...'


# if mani module to execute
if __name__ == '__main__':
    # set connections
    (rest_ses, flag) = get_db_connection()
    # add restaurant
    init_all_tables(rest_ses)
    
    

