"use strict";

const MISSING_IMAGE_URL = "https://tinyurl.com/tv-missing";
const TVMAZE_API_URL = "https://api.tvmaze.com";

const $showsList = $("#showsList");
const $episodesList = $("#episodesList");
const $episodesArea = $("#episodesArea");
const $searchForm = $("#searchForm");



/** Given a search term, search for tv shows that match that query.
 *
 *  Returns (promise) array of show objects: [show, show, ...].
 *    Each show object should contain exactly: {id, name, summary, image}
 *    (if no image URL given by API, put in a default image URL)
 */

async function getShowsByTerm(term) {
  //    Make request to TVMaze search shows API.
  //    Make an array of objects based on returned list of shows.
  //    Return array-of-shows promise.
  const response = await axios ({ 
    baseURL: TVMAZE_API_URL,
    url: "search/shows",
    method: "GET",
    params: {
      q: term,
    },
  });

  return response.data.map(result => {
    const show = result.show;
    return {
      id: show.id,
      name: show.name,
      premiered: show.premiered,
      summary: show.summary,
      image: show.image ? show.image.medium : MISSING_IMAGE_URL
    };
  });
}


/** Given list of shows, create markup for each and to DOM */

function populateShows(shows) {
  $showsList.empty();

  for (let show of shows) {
    const $show = $(`
      <div data-show-id="${show.id}" class="Show col-md-12 col-lg-6 mb-4">
         <div class="media">
           <img src="${show.image}" alt="${show.name}" class="w-25 me-3">
           <div class="media-body">
             <h4 class="text-primary">${show.name}</h4>
             <h6 class="text-primary">Premiered: ${show.premiered}</h6>
             <div><small>${show.summary}</small></div>
              <button class="btn btn-primary btn-sm Show-getEpisodes">Episodes</button>
           </div>
         </div>
       </div>
      `);
    $showsList.append($show);
  }
}


/** Handle search form submission: get shows from API and display.
 *    Hide episodes area (that only gets shown if they ask for episodes)
 */

async function searchForShowAndDisplay() {
  const term = $("#searchForm-term").val();
  const shows = await getShowsByTerm(term);

  $episodesArea.hide();
  populateShows(shows);
}

$searchForm.on("submit", async function (evt) {
  evt.preventDefault();
  await searchForShowAndDisplay();
});


/** Given a show ID, get from API and return (promise) array of episodes:
 *      { id, name, season, number }
 */

async function getEpisodesOfShow(id) { 
  const response = await axios ({ 
    baseURL: TVMAZE_API_URL,
    url: `shows/${id}/episodes`,
    method: "GET",
  });

  return response.data.map(e => ({
    id: e.id,
    name: e.name,
    season: e.season,
    number: e.number,
  }));
}

/** Given list of episodes, create markup for each and append to DOM  */

function populateEpisodes(episodes) { 
  $episodesList.empty();

  for (let episode of episodes) {
    const $episodesTable = $(
      ` <tr class="d-flex">
          <td class="col-4">${episode.name}</td>
          <td class="col-1">${episode.season}</td>
          <td class="col-1">${episode.number}</td>
        </tr>
      `
    );
    $episodesList.append($episodesTable);
  }
  $episodesArea.show();
}


/** Handle click of episodes list: show details */
async function getEpisodesAndDisplay(evt) {
  const showId = $(evt.target).closest("[data-show-id]").data("show-id");
  const episodes = await getEpisodesOfShow(showId);
  populateEpisodes(episodes);
}

$showsList.on("click", ".Show-getEpisodes", getEpisodesAndDisplay);

