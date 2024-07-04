let libPrefix = 'ResourcesLib_';

let growthResource = function(resource){
  return {
    resource: resource,

    /// auto growthing or decreasing
    propName: function(){ return this.resource.propName() + '_growth'},

    info: function(){
      return Bot.getProperty(this.propName()) || {}
    },

    title: function(){
      if(!this.isEnabled){ return }

      let growth = this.info();
      let start_text = 'add ' + String(growth.increment);
      let middle_text = ' once at ' + String(growth.interval) + ' secs';

      if(growth.type=='simple'){
        return  start_text + middle_text
      }
      if(growth.type=='percent'){
        return  start_text + '%' + middle_text
      }
      if(growth.type=='compound_interest'){
        return  start_text + '%' + middle_text + ' with reinvesting'
      }
    },

    have: function(){ return this.info() },

    isEnabled: function(){
      let growth = this.info();
      if(growth){ return growth.enabled }
      return false;
    },
    
    _toggle: function(status){
      let growth = this.info();
      if(!growth){ return }

      growth.enabled = status;
      return Bot.setProperty(this.propName(), growth, 'json');
    },

    stop: function(){
      return this._toggle(false);
    },

    progress: function(){
      let growth = this.info();
      if(!growth){ return }

      let total_iterations = this.totalIterations(growth);
      let fraction = total_iterations % 1;
      return fraction*100;
    },

    willCompletedAfter: function(){
      return this.info().interval - this.progress()/100 * this.info().interval;
    },

    totalIterations: function(growth){
      if(!growth){ growth = this.info() }

      let now = (new Date().getTime());
      let duration_in_seconds = ( now - growth.started_at ) / 1000;
      return duration_in_seconds / growth.interval;
    },

    _calcMinMax(result, growth){
      if((growth.min)&&(growth.min > result)){
        return growth.min
      }

      if((growth.max)&&(growth.max < result)){
        return growth.max
      }

      return result
    },

    _calcByTotalIterations(value, total_iterations, growth){
      var result;
      if(growth.type=='simple'){
        result = value + total_iterations * growth.increment
      }
      if(growth.type=='percent'){
        let percent =  growth.increment / 100;
        let all_percents =  percent * growth.base_value * total_iterations
        result = value + all_percents;
      }
      if(growth.type=='compound_interest'){
        let percent = (1 + growth.increment / 100);
        result = value * Math.pow(percent, total_iterations)
      }
      return result;
    },

    _getTotalIterationsWithLimit(growth){
      let total_iterations = this.totalIterations(growth);

      if(!growth.max_iterations_count){ return total_iterations }

      let total = total_iterations + growth.completed_iterations_count;
      if(total < growth.max_iterations_count){
        return total_iterations
      }
      
      return growth.max_iterations_count - growth.completed_iterations_count;
    },

    _calcValue(value, growth){
      let total_iterations = this._getTotalIterationsWithLimit(growth);

      if(total_iterations<1){ return }

      let fraction = total_iterations % 1;
      total_iterations = total_iterations - fraction;

      var result = this._calcByTotalIterations(value, total_iterations, growth)

      growth.completed_iterations_count+= total_iterations;
      
      result = this._calcMinMax(result, growth);
      
      this._updateIteration(growth, fraction * 1000);

      return result;
    },

    getValue: function(value){
      let growth = this.info();
      if(!growth){ return value }
      if(!growth.enabled){ return value }

      let new_value = this._calcValue(value, growth);

      if(!new_value){ return value }

      this.resource._set(new_value);  /// update value

      return new_value;
    },

    _updateIteration: function(growth, fraction){
      if(!growth){ growth = this.info() }
      if(!growth){ return }

      let started_at = (new Date().getTime());
      /// started same early
      if(fraction){ started_at = started_at - fraction }

      growth.started_at = started_at;

      return Bot.setProperty(this.propName(), growth, 'json');
    },

    _updateBaseValue: function(base_value){
      var growth = this.info();
      if(!growth){ return }

      growth.base_value = base_value;
      return Bot.setProperty(this.propName(), growth, 'json');
    },

    _newGrowth: function(options){
      return {
        base_value: this.resource.baseValue(),
        increment: options.increment,
        interval: options.interval,
        type: options.type,
        min: options.min,
        max: options.max,
        max_iterations_count: options.max_iterations_count,
        enabled: true,
        completed_iterations_count: 0
      }
    },

    _addAs: function(options){
      let growth = this._newGrowth(options);
      return this._updateIteration(growth);
    },

    add: function(options){
      /// absolute growth value
      options.type = 'simple';
      options.increment = options.value;
      return this._addAs(options);
    },

    addPercent: function(options){
      /// percent
      options.type = 'percent';
      options.increment = options.percent;
      return this._addAs(options);
    },

    addCompoundInterest: function(options){
      /// compound percent
      options.type = 'compound_interest';
      options.increment = options.percent;
      return this._addAs(options);
    }

  }
}

let commonResource = function(objName, objID, resName){
  return {
    objName: objName,
    objID: objID,
    name: resName,
    growth: null,

    _setGrowth: function(growth){
      this.growth = growth;
    },

    propName: function(){
      return libPrefix + this.objName + this.objID + '_' + this.name
    },

    isNumber: function(value){ return typeof(value)=='number' },

    verifyNumber: function(value){ 
      if(!this.isNumber(value)){
        let evalue = '';
        if(typeof(value)!='undefined'){ evalue = JSON.stringify(value) }
        throw 'ResLib: value must be number only. It is not number: ' + typeof(value) + ' ' + evalue;
      }
    },

    removeRes: function(res_amount){
      this.set(this.value() - res_amount);
      return true;
    },

    baseValue: function(){
      let cur_value = Bot.getProperty(this.propName());
      if(typeof(cur_value)=='undefined'){ return 0 }

      return cur_value;
    },

    value: function(){
      let cur_value = this.baseValue();

      if(this._withEnabledGrowth()){
        return this.growth.getValue(cur_value);
      }
      return cur_value;
    },
    
    add: function(res_amount){
      this.verifyNumber(res_amount);
      this.set(this.value() + res_amount)
      return true;
    },

    have: function(res_amount){
      this.verifyNumber(res_amount);
      // can not have negative or null amount
      if(res_amount < 0){ return false }
      if(res_amount == 0){ return false }

      return this.value() >= res_amount;
    },
    
    remove: function(res_amount){
      if(!this.have(res_amount)){
        throw 'ResLib: not enough resources'
      }
      return this.removeRes(res_amount);
    },
    
    removeAnyway: function(res_amount){
      this.verifyNumber(res_amount);
      return this.removeRes(res_amount)
    },

    _withEnabledGrowth: function(){
      return (this.growth && this.growth.isEnabled())
    },

    _set: function(res_amount){
      Bot.setProperty(this.propName(), res_amount, 'float');
    },

    set: function(res_amount){
      this.verifyNumber(res_amount);

      if( this._withEnabledGrowth() ){
        this.growth._updateBaseValue(res_amount)
      }
      return this._set(res_amount);
    },

    anywayTakeFromAndTransferTo: function(fromResource, toResource, res_amount){
      if(fromResource.name!=toResource.name){
        throw 'ResLib: can not transfer different resources'
      }

      if(fromResource.removeAnyway(res_amount)){
        return toResource.add(res_amount)
      }
      return false
    },

    anywayTakeFromAndTransferToDifferent: function(fromResource, toResource, remove_amount, add_amount){
      if(fromResource.removeAnyway(remove_amount)){
        return toResource.add(add_amount)
      }
      return false
    },

    takeFromAndTransferTo: function(fromResource, toResource, res_amount){
      if(!fromResource.have(res_amount)){
        throw 'ResLib: not enough resources for transfer'
      }

      return this.anywayTakeFromAndTransferTo(fromResource, toResource, res_amount)
    },

    takeFromAndTransferToDifferent: function(fromResource, toResource, remove_amount, add_amount){
      if(!fromResource.have(remove_amount)){
        throw 'ResLib: not enough resources for transfer'
      }

      return this.anywayTakeFromAndTransferToDifferent(fromResource, toResource, remove_amount, add_amount)
    },

    takeFromAnother: function(anotherResource, res_amount){
      return this.takeFromAndTransferTo(anotherResource, this, res_amount);
    },

    transferTo: function(anotherResource, res_amount){
      return this.takeFromAndTransferTo(this, anotherResource, res_amount);
    },

    exchangeTo: function(anotherResource, options){
      return this.takeFromAndTransferToDifferent(this, 
        anotherResource, options.remove_amount, options.add_amount );
    },

    takeFromAnotherAnyway: function(anotherResource, res_amount){
      return this.anywayTakeFromAndTransferTo(anotherResource, this, res_amount);
    },

    transferToAnyway: function(anotherResource, res_amount){
      return this.anywayTakeFromAndTransferTo(this, anotherResource, res_amount);
    }

  }
}

let growthFor = function(resource){
  let growth = growthResource(resource);
  resource._setGrowth(growth);
  return growth;
}

let getResourceFor = function(object, object_id, resName){
  let res =  commonResource(object, object_id, resName);
  growthFor(res);

  return res;
}

let userResource = function(resName){
  return getResourceFor('user', user.telegramid, resName);
}

let chatResource = function(resName){
  return getResourceFor('chat', chat.chatid, resName);
}

let anotherUserResource = function(resName, telegramid){
  return getResourceFor('user', telegramid, resName);
}

let anotherChatResource = function(resName, chatid){
  return getResourceFor('chat', chatid, resName);
}



publish({
  userRes: userResource,
  chatRes: chatResource,

  anotherUserRes: anotherUserResource,
  anotherChatRes: anotherChatResource,

  growthFor: growthFor

})